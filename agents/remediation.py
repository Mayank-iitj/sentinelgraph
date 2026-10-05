from agents.llm import LLMClient
from agents.prompts import REMEDIATION_SYSTEM_PROMPT

class RemediationAgent:
    def __init__(self, mcp_client):
        self.llm = LLMClient()
        self.mcp_client = mcp_client
        
    def remediate(self, investigation_result: dict, dry_run: bool = False) -> dict:
        if self.llm.offline:
            return {
                "status": "remediated" if not dry_run else "dry_run",
                "actions": [
                    {"type": "ticket_created", "assignee": investigation_result.get("owner", "unknown")},
                    {"type": "playbook_drafted", "steps": ["Isolate host", "Block IP"]}
                ]
            }
            
        messages = [{"role": "user", "content": f"Remediate based on: {investigation_result}"}]
        # Tool loop calling `create_ticket`, `draft_containment`
        return {"status": "completed"}
