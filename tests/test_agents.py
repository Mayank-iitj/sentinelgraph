from agents.llm import LLMClient
from agents.triage import TriageAgent
from agents.investigator import InvestigatorAgent
from agents.remediation import RemediationAgent
from agents.memory_agent import MemoryAgent
from agents.orchestrator import Orchestrator


def test_llm_offline_stub():
    llm = LLMClient()
    if llm.offline:
        res = llm.generate("system", [{"role": "user", "content": "test"}])
        assert res["role"] == "assistant"
        assert "Offline response stub" in res["content"][0]["text"]


def test_triage_agent_offline():
    agent = TriageAgent(None)
    res = agent.run_triage([{"id": "finding_1", "risk_score": 6.0}])
    assert len(res) == 1
    assert res[0].verdict == "act"


def test_triage_agent_ignore():
    agent = TriageAgent(None)
    res = agent.run_triage([{"id": "finding_2", "risk_score": 2.0}])
    assert len(res) == 1
    assert res[0].verdict == "ignore"


def test_investigator_offline():
    agent = InvestigatorAgent(None)
    res = agent.investigate("finding_true_0")
    assert res["finding_id"] == "finding_true_0"
    assert res["owner"] == "User 0"


def test_remediation_offline():
    agent = RemediationAgent(None)
    inv = {"owner": "User 0", "finding_id": "test"}
    res = agent.remediate(inv)
    assert res["status"] == "remediated"
    assert len(res["actions"]) == 2


def test_remediation_dry_run():
    agent = RemediationAgent(None)
    res = agent.remediate({"owner": "User 0"}, dry_run=True)
    assert res["status"] == "dry_run"


def test_memory_agent_offline():
    agent = MemoryAgent(None)
    res = agent.process_session("test_session")
    assert res["status"] == "memory_consolidated"
    assert res["new_facts"] == 1


def test_memory_agent_retrieve():
    agent = MemoryAgent(None)
    res = agent.retrieve_context("kafka")
    assert "kafka" in res["context"].lower()


def test_orchestrator_init():
    orch = Orchestrator()
    assert orch.triage is not None
    assert orch.investigator is not None
    assert orch.remediation is not None
    assert orch.memory is not None


def test_full_pipeline_offline():
    """End-to-end: Triage → Investigate → Remediate → Memory"""
    orch = Orchestrator()

    verdicts = orch.triage.run_triage(
        [
            {"id": "finding_true_0", "risk_score": 9.5},
            {"id": "finding_decoy_0", "risk_score": 1.0},
        ]
    )
    assert len(verdicts) == 2

    act_findings = [v for v in verdicts if v.verdict == "act"]
    ignore_findings = [v for v in verdicts if v.verdict == "ignore"]
    assert len(act_findings) == 1
    assert len(ignore_findings) == 1

    inv = orch.investigator.investigate(act_findings[0].id)
    assert inv["owner"] == "User 0"

    rem = orch.remediation.remediate(inv)
    assert rem["status"] == "remediated"

    mem = orch.memory.process_session("test")
    assert mem["status"] == "memory_consolidated"
