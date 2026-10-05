from graph.queries import GraphClient
import uuid

class EpisodicMemory:
    """Manages Session, Message, and ToolCall nodes (episodic memory)."""
    def __init__(self, tenant_id: str = "tenant_1"):
        self.client = GraphClient(tenant_id)
        
    def add_message(self, session_id: str, role: str, content: str):
        msg_id = str(uuid.uuid4())
        query = """
        MATCH (s:Session {id: $sid})
        CREATE (m:Message {id: $mid, role: $role, content: $content, ts: timestamp()})
        CREATE (s)-[:HAS_MESSAGE]->(m)
        """
        self.client.run_query(query, {'sid': session_id, 'mid': msg_id, 'role': role, 'content': content})
        return msg_id
        
    def add_tool_call(self, message_id: str, tool_name: str, args: str, result: str):
        tc_id = str(uuid.uuid4())
        query = """
        MATCH (m:Message {id: $mid})
        CREATE (tc:ToolCall {id: $tcid, name: $name, args: $args, result: $result, ts: timestamp()})
        CREATE (m)-[:CALLED]->(tc)
        """
        self.client.run_query(query, {'mid': message_id, 'tcid': tc_id, 'name': tool_name, 'args': args, 'result': result})
        return tc_id
