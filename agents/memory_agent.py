from agents.llm import LLMClient


class MemoryAgent:
    def __init__(self, mcp_client):
        self.llm = LLMClient()
        self.mcp_client = mcp_client

    def process_session(self, session_id: str):
        # Reads the session messages, extracts facts, supersedes old ones
        if self.llm.offline:
            return {"status": "memory_consolidated", "new_facts": 1, "superseded": 0}

        # Tool loop calling `remember_fact`, `session_history`
        return {"status": "completed"}

    def retrieve_context(self, query: str):
        if self.llm.offline:
            return {"context": "Retrieved context for query: " + query}
        # Uses `recall`, `find_similar_incidents`
        return {"context": "..."}
