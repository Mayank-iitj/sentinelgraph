from mcp.server.fastmcp import FastMCP
from graph.queries import GraphClient
import json


def format_result(data, evidence="", path=[]):
    return json.dumps({"result": data, "evidence": evidence, "path": path})


def register_brain_tools(mcp: FastMCP):
    client = GraphClient()

    @mcp.tool()
    def who_owns(service: str) -> str:
        query = "MATCH (t:Team)-[:OWNS]->(s:Service {id: $svc}) RETURN t"
        res = client.run_query(query, {"svc": service})
        return format_result(res, evidence=f"Found owner for {service}.")

    @mcp.tool()
    def who_knows(service: str, limit: int = 5) -> str:
        # Ranked by KNOWS_ABOUT or authorship
        query = """
        MATCH (p:Person)-[:AUTHORED]->(d:Document)
        WHERE d.content CONTAINS $svc
        RETURN p.id, p.name, count(d) as score
        ORDER BY score DESC LIMIT $limit
        """
        res = client.run_query(query, {"svc": service, "limit": limit})
        return format_result(res, evidence=f"Found experts for {service}.")

    @mcp.tool()
    def trace_decision(topic_or_id: str) -> str:
        # decision -> rationale -> source span
        query = "MATCH (d:Decision)-[:DECIDED_IN]->(doc:Document) WHERE d.id = $id OR d.summary CONTAINS $id RETURN d, doc.source_id, doc.content"
        res = client.run_query(query, {"id": topic_or_id})
        return format_result(res, evidence="Decision traced.")

    @mcp.tool()
    def what_changed(service: str, since: str) -> str:
        query = "MATCH (d:Decision)-[:DECIDED_IN]->(doc:Document) WHERE doc.content CONTAINS $svc AND d.date >= $since RETURN d"
        res = client.run_query(query, {"svc": service, "since": since})
        return format_result(res, evidence="Changes found.")

    @mcp.tool()
    def find_stale_knowledge() -> str:
        query = "MATCH (new:Decision)-[:SUPERSEDES]->(old:Decision) WHERE old.status = 'active' RETURN old"
        res = client.run_query(query)
        return format_result(res, evidence="Stale knowledge identified.")

    @mcp.tool()
    def route_to_owner(finding_id: str) -> str:
        query = """
        MATCH (f:Finding {id: $fid})-[:AFFECTS]->(a:Asset)-[:RUNS]->(s:Service)<-[:OWNS]-(t:Team)<-[:MEMBER_OF]-(p:Person)
        RETURN p LIMIT 1
        """
        res = client.run_query(query, {"fid": finding_id})
        return format_result(res, evidence="Routed finding to owner.")
