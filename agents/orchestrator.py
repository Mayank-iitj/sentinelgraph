import uuid
from graph.queries import GraphClient
from agents.triage import TriageAgent
from agents.investigator import InvestigatorAgent
from agents.remediation import RemediationAgent
from agents.memory_agent import MemoryAgent

class Orchestrator:
    def __init__(self):
        self.client = GraphClient()
        self.triage = TriageAgent(None)
        self.investigator = InvestigatorAgent(None)
        self.remediation = RemediationAgent(None)
        self.memory = MemoryAgent(None)
        
    def claim_task(self, task_type: str, agent_name: str) -> str:
        # Atomic claim using Cypher
        query = """
        MATCH (t:AgentTask {type: $type, status: 'pending'})
        WITH t LIMIT 1
        SET t.status = 'in_progress', t.claimed_by = $agent
        RETURN t.id
        """
        res = self.client.run_query(query, {'type': task_type, 'agent': agent_name})
        if res and res[0]:
            return res[0][0]
        return None
        
    def handoff(self, from_task: str, to_type: str, payload: dict):
        new_id = str(uuid.uuid4())
        query = """
        MATCH (old:AgentTask {id: $old_id})
        CREATE (new:AgentTask {id: $new_id, type: $type, status: 'pending', payload: $payload})
        CREATE (old)-[:HANDED_OFF_TO {ts: timestamp()}]->(new)
        SET old.status = 'completed'
        """
        self.client.run_query(query, {'old_id': from_task, 'new_id': new_id, 'type': to_type, 'payload': str(payload)})
        return new_id
