from agents.llm import LLMClient
from agents.prompts import INVESTIGATOR_SYSTEM_PROMPT
import json

class InvestigatorAgent:
    def __init__(self, mcp_client):
        self.llm = LLMClient()
        self.mcp_client = mcp_client
        
    def investigate(self, finding_id: str) -> dict:
        # Pseudo implementation for full pipeline
        if self.llm.offline:
            return {
                "finding_id": finding_id,
                "context": "Expanded graph context found. Root cause traced to ADR 001.",
                "owner": "User 0",
                "team": "Team 0"
            }
            
        messages = [{"role": "user", "content": f"Investigate finding {finding_id}"}]
        # Tool call loop would go here calling `who_owns`, `trace_decision`, `cluster_alerts`
        return {"status": "investigated", "finding_id": finding_id}
