from brain.ingest import BrainIngestor
from brain.extract import BrainExtractor
from brain.provenance import ProvenanceTracker

class BrainToolkit:
    def __init__(self, tenant_id: str = "tenant_1"):
        self.ingestor = BrainIngestor(tenant_id)
        self.extractor = BrainExtractor(tenant_id)
        self.provenance = ProvenanceTracker(tenant_id)
        
    def process_new_document(self, title: str, path: str, content: str, author_id: str):
        doc_id = self.ingestor.ingest_document(title, path, content, author_id)
        decisions = self.extractor.extract_decisions(doc_id, content)
        for dec in decisions:
            self.extractor.link_decision_to_doc(dec["id"], doc_id, dec["summary"], dec["rationale"])
        return doc_id
