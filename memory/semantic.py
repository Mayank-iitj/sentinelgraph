from graph.queries import GraphClient
import uuid
import datetime

class SemanticMemory:
    """Manages Facts with bitemporal supersession (semantic memory)."""
    def __init__(self, tenant_id: str = "tenant_1"):
        self.client = GraphClient(tenant_id)
        
    def remember(self, statement: str, confidence: float = 1.0, supersedes_id: str = None):
        fid = str(uuid.uuid4())
        ts = datetime.datetime.now().isoformat()
        
        self.client.run_query(
            "CREATE (f:Fact {id: $fid, statement: $stmt, confidence: $conf, valid_from: $ts})",
            {'fid': fid, 'stmt': statement, 'conf': confidence, 'ts': ts}
        )
        
        if supersedes_id:
            self.client.run_query(
                "MATCH (old:Fact {id: $old_id}), (new:Fact {id: $new_id}) CREATE (new)-[:SUPERSEDES]->(old) SET old.valid_to = $ts",
                {'old_id': supersedes_id, 'new_id': fid, 'ts': ts}
            )
        return fid
