from graph.queries import GraphClient

class ProvenanceTracker:
    def __init__(self, tenant_id: str = "tenant_1"):
        self.client = GraphClient(tenant_id)
        
    def get_source_spans(self, node_id: str):
        res = self.client.run_query(
            "MATCH (n {id: $id})-[r:DECIDED_IN|AUTHORED|MENTIONS*1..3]-(doc:Document) RETURN doc.source_id, doc.path, doc.content",
            {'id': node_id}
        )
        return res
