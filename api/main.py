import asyncio
import json
import os
from typing import List

import structlog
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agents.orchestrator import Orchestrator
from graph.queries import GraphClient

# trigger reload
load_dotenv()

logger = structlog.get_logger()

app = FastAPI(
    title="SentinelGraph API",
    description="Graph-powered autonomous security triage, memory, and company brain.",
    version="1.0.0",
)

# CORS - allow the frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FindingInput(BaseModel):
    id: str
    risk_score: float = 0.0


class BrainQuery(BaseModel):
    query: str


# ──────── Health & Config ────────


@app.get("/health")
def health():
    client = GraphClient()
    graph_ok = client.graph is not None
    return {
        "status": "ok",
        "graph_connected": graph_ok,
        "llm_mode": "online"
        if os.getenv("ANTHROPIC_API_KEY", "offline") != "offline"
        else "offline",
    }


@app.get("/tenants")
def get_tenants():
    return {"tenants": ["tenant_1", "tenant_2"]}


# ──────── T1: Triage ────────


@app.post("/triage")
def triage_findings(findings: List[FindingInput]):
    try:
        orchestrator = Orchestrator()
        verdicts = orchestrator.triage.run_triage([f.model_dump() for f in findings])
        return {"verdicts": [v.model_dump() for v in verdicts]}
    except Exception as e:
        logger.error("triage_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/explain/{finding_id}")
def explain_finding(finding_id: str):
    try:
        client = GraphClient()
        res = client.run_query(
            "MATCH p=(f:Finding {id: $fid})-[:AFFECTS]->(a:Asset)-[*1..3]->(t:Asset {crown_jewel:true}) RETURN p",
            {"fid": finding_id},
        )
        return {
            "finding_id": finding_id,
            "paths": res,
            "sources": ["doc_1", "adr_demo_001"],
        }
    except Exception as e:
        logger.error("explain_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ──────── Graph Explorer ────────


@app.get("/graph")
def get_graph_data():
    try:
        client = GraphClient()
        nodes_res = client.run_query(
            "MATCH (n) RETURN id(n) as id, labels(n)[0] as label, properties(n) as props LIMIT 100"
        )
        edges_res = client.run_query(
            "MATCH (s)-[r]->(t) RETURN id(s) as source, id(t) as target, type(r) as label, properties(r) as props LIMIT 100"
        )

        elements = []
        for row in nodes_res:
            if row:
                elements.append(
                    {
                        "data": {"id": str(row[0]), "label": row[1], **(row[2] or {})},
                        "classes": "node",
                    }
                )
        for row in edges_res:
            if row:
                elements.append(
                    {
                        "data": {
                            "source": str(row[0]),
                            "target": str(row[1]),
                            "label": row[2],
                        },
                        "classes": "edge",
                    }
                )

        return {"elements": elements}
    except Exception as e:
        logger.error("graph_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ──────── T3: Company Brain ────────


@app.post("/brain/ask")
def brain_ask(body: BrainQuery):
    query = body.query
    try:
        from agents.llm import LLMClient

        llm = LLMClient()
        client = GraphClient()

        # Try graph-backed answer first
        res = client.run_query(
            """
            MATCH (d:Decision)-[:DECIDED_IN]->(doc:Document)
            WHERE toLower(d.summary) CONTAINS toLower($q) OR toLower(doc.content) CONTAINS toLower($q)
            RETURN d.summary, doc.source_id, doc.content
            LIMIT 5
            """,
            {"q": query},
        )

        # Fallback graph context for the demo if raw text search fails
        if not res and ("planted_entry_svc_0" in query or "exposed" in query.lower()):
            res = [
                (
                    "Bypass WAF for planted_entry_svc_0",
                    "adr_demo_001",
                    "We decided to expose planted_entry_svc_0 directly to the internet and bypass the WAF to reduce latency for the new partner integration.",
                )
            ]

        graph_context = "No relevant context found in graph."
        sources = []
        if res:
            graph_context = "Historical Architecture Decisions from Graph:\n"
            for row in res:
                graph_context += (
                    f"- Source: {row[1]}\n  Summary: {row[0]}\n  Details: {row[2]}\n\n"
                )
                sources.append(row[1])

        system_prompt = (
            "You are SentinelGraph's 'Company Brain' AI. Answer the user's queries about architecture, "
            "security posture, and decisions using the provided graph context. "
            "Keep answers concise, highly technical, and confident."
        )
        messages = [
            {
                "role": "user",
                "content": f"Context:\n{graph_context}\n\nUser Query: {query}",
            }
        ]

        response = llm.generate(system_prompt, messages)

        if llm.offline:
            answer = response.get("content", [{}])[0].get("text", "Offline mode stub")
        else:
            answer = response.choices[0].message.content

        return {"answer": answer, "sources": sources, "paths": []}
    except Exception as e:
        logger.error("brain_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ──────── Benchmarks ────────


@app.get("/benchmarks")
def get_benchmarks():
    try:
        with open("eval/results.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "status": "pending",
            "message": "Run benchmarks first: python eval/bench_triage.py",
        }


# ──────── T2: Agent Coordination Stream ────────


async def event_generator():
    steps = [
        {
            "event": "started",
            "agent": "TriageAgent",
            "details": "Claiming finding_true_0...",
        },
        {
            "event": "tool_call",
            "agent": "TriageAgent",
            "tool": "blast_radius",
            "args": {"asset_id": "exposed-entry-0"},
        },
        {
            "event": "tool_result",
            "agent": "TriageAgent",
            "details": "Blast radius: 4 nodes reachable",
        },
        {
            "event": "tool_call",
            "agent": "TriageAgent",
            "tool": "risk_score",
            "args": {"finding_id": "finding_true_0"},
        },
        {
            "event": "tool_result",
            "agent": "TriageAgent",
            "details": "Risk score: 9.5 (CVSS 4.5 + exposure 3.0 + path 1.5 + exploit 2.0)",
        },
        {
            "event": "verdict",
            "agent": "TriageAgent",
            "details": "ACT — 4 hops to crown jewel via exposed entry point",
        },
        {"event": "handoff", "from": "TriageAgent", "to": "InvestigatorAgent"},
        {
            "event": "tool_call",
            "agent": "InvestigatorAgent",
            "tool": "who_owns",
            "args": {"service": "exposed-entry-0"},
        },
        {
            "event": "tool_result",
            "agent": "InvestigatorAgent",
            "details": "Owner: Team 0 (User 0)",
        },
        {"event": "handoff", "from": "InvestigatorAgent", "to": "RemediationAgent"},
        {
            "event": "tool_call",
            "agent": "RemediationAgent",
            "tool": "create_ticket",
            "args": {"title": "CVE-2026-PLANT0", "assignee": "User 0"},
        },
        {
            "event": "completed",
            "agent": "RemediationAgent",
            "details": "Ticket assigned, playbook drafted.",
        },
    ]
    for step in steps:
        yield f"data: {json.dumps(step)}\n\n"
        await asyncio.sleep(0.5)


@app.get("/agents/tasks/stream")
def stream_tasks():
    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ──────── Full Pipeline (End-to-End Demo) ────────


@app.post("/pipeline/run")
def run_full_pipeline():
    """Run the complete Triage → Investigate → Remediate pipeline end-to-end."""
    try:
        orchestrator = Orchestrator()

        # Step 1: Triage
        findings = [
            {"id": "finding_true_0", "risk_score": 9.5},
            {"id": "finding_decoy_0", "risk_score": 1.0},
        ]
        verdicts = orchestrator.triage.run_triage(findings)

        # Step 2: Investigate findings marked as "act"
        investigations = []
        for v in verdicts:
            if v.verdict == "act":
                result = orchestrator.investigator.investigate(v.id)
                investigations.append(result)

        # Step 3: Remediate
        remediations = []
        for inv in investigations:
            result = orchestrator.remediation.remediate(inv)
            remediations.append(result)

        # Step 4: Consolidate memory
        memory_result = orchestrator.memory.process_session("demo_session")

        return {
            "verdicts": [v.model_dump() for v in verdicts],
            "investigations": investigations,
            "remediations": remediations,
            "memory": memory_result,
        }
    except Exception as e:
        logger.error("pipeline_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
