from graph.queries import GraphClient
import uuid
import datetime

class BrainIngestor:
    """Ingests documents/tickets/chats into the Company Brain."""
    def __init__(self, tenant_id: str = "tenant_1"):
        self.client = GraphClient(tenant_id)
        
    def ingest_document(self, title: str, path: str, content: str, author_id: str):
        doc_id = str(uuid.uuid4())
        ts = datetime.datetime.now().isoformat()
        
        # Idempotent upsert logic could go here via MERGE, but for simplicity:
        self.client.run_query(
            "CREATE (d:Document {id: $did, title: $title, path: $path, updated_at: $ts, content: $content, source_id: $did})",
            {'did': doc_id, 'title': title, 'path': path, 'ts': ts, 'content': content}
        )
        
        if author_id:
            self.client.run_query(
                "MATCH (p:Person {id: $pid}), (d:Document {id: $did}) CREATE (p)-[:AUTHORED]->(d)",
                {'pid': author_id, 'did': doc_id}
            )
        return doc_id
