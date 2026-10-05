from agents.llm import LLMClient
from agents.prompts import TRIAGE_SYSTEM_PROMPT
from agents.schemas import FindingVerdict
import json

class TriageAgent:
    def __init__(self, mcp_client):
        self.llm = LLMClient()
        self.mcp_client = mcp_client # Mocked or real MCP client to call tools
        
    def run_triage(self, findings: list) -> list[FindingVerdict]:
        results = []
        for finding in findings:
            messages = [
                {"role": "user", "content": f"Analyze finding: {json.dumps(finding)}"}
            ]
            
            # Simple stub logic for when offline or simplified graph
            if self.llm.offline:
                score = finding.get('risk_score', 0.0)
                verdict = "act" if score > 5.0 else "ignore"
                fv = FindingVerdict(
                    id=finding['id'],
                    asset="mock_asset",
                    risk_score=score,
                    rank=1,
                    verdict=verdict,
                    reasoning="Offline stub execution.",
                    path=[],
                    sources=[]
                )
                results.append(fv)
                continue
                
            # In a real implementation with Anthropic tool use, we'd loop up to 12 times:
            # response = self.llm.generate(TRIAGE_SYSTEM_PROMPT, messages, tools=self.mcp_client.get_tools())
            # while response.stop_reason == "tool_use":
            #    ... call tool, append to messages, loop
            
            # Here we mock the structured output for now since we need a fast deterministic end-to-end
            # Let's say we do a manual lookup for risk_score using the mcp_client if it's available
            
            # Dummy result for now
            results.append(FindingVerdict(
                id=finding.get('id', 'unknown'),
                asset='unknown',
                risk_score=0.0,
                rank=99,
                verdict='ignore',
                reasoning='Dummy',
                path=[]
            ))
            
        return sorted(results, key=lambda x: x.rank)
