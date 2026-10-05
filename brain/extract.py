from agents.llm import LLMClient
from graph.queries import GraphClient
import uuid

class BrainExtractor:
    def __init__(self, tenant_id: str = "tenant_1"):
        self.llm = LLMClient()
        self.client = GraphClient(tenant_id)
        
    def extract_decisions(self, doc_id: str, content: str):
        if self.llm.offline:
            return [{"id": "stub_dec", "summary": "Offline decision extract", "rationale": "Testing."}]
            
        # Use LLM to extract structured decisions from text
        # ... implementation ...
        return []
        
    def link_decision_to_doc(self, dec_id: str, doc_id: str, summary: str, rationale: str):
        self.client.run_query(
            "CREATE (d:Decision {id: $did, summary: $sum, rationale: $rat, date: timestamp(), status: 'active', source_id: $doc_id})",
            {'did': dec_id, 'sum': summary, 'rat': rationale, 'doc_id': doc_id}
        )
        self.client.run_query(
            "MATCH (dec:Decision {id: $did}), (doc:Document {id: $doc_id}) CREATE (dec)-[:DECIDED_IN]->(doc)",
            {'did': dec_id, 'doc_id': doc_id}
        )
