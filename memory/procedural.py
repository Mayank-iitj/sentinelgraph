from graph.queries import GraphClient
import uuid
import json


class ProceduralMemory:
    """Manages Playbooks (procedural memory)."""

    def __init__(self, tenant_id: str = "tenant_1"):
        self.client = GraphClient(tenant_id)

    def save_playbook(self, incident_id: str, steps: list, success: bool):
        pid = str(uuid.uuid4())
        sc = 1 if success else 0
        fc = 0 if success else 1

        self.client.run_query(
            "CREATE (p:Playbook {id: $pid, steps: $steps, success_count: $sc, failure_count: $fc})",
            {"pid": pid, "steps": json.dumps(steps), "sc": sc, "fc": fc},
        )
        self.client.run_query(
            "MATCH (i:Incident {id: $id}), (p:Playbook {id: $pid}) CREATE (i)-[:RESOLVED_BY]->(p)",
            {"id": incident_id, "pid": pid},
        )
        return pid

    def get_playbook(self, incident_id: str):
        res = self.client.run_query(
            "MATCH (i:Incident {id: $id})-[:RESOLVED_BY]->(p:Playbook) RETURN p",
            {"id": incident_id},
        )
        return res
