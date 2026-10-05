from mcp.server.fastmcp import FastMCP
from graph.queries import GraphClient
import json
import uuid
import datetime

def format_result(data, evidence="", path=[]):
    return json.dumps({"result": data, "evidence": evidence, "path": path})

def register_memory_tools(mcp: FastMCP):
    client = GraphClient()

    @mcp.tool()
    def remember_fact(fact_statement: str, confidence: float = 1.0, supersedes_fact_id: str = None) -> str:
        fid = str(uuid.uuid4())
        ts = datetime.datetime.now().isoformat()
        
        query = "CREATE (f:Fact {id: $fid, statement: $stmt, confidence: $conf, valid_from: $ts})"
        client.run_query(query, {'fid': fid, 'stmt': fact_statement, 'conf': confidence, 'ts': ts})
        
        if supersedes_fact_id:
            query2 = """
            MATCH (old:Fact {id: $old_id}), (new:Fact {id: $new_id})
            CREATE (new)-[:SUPERSEDES]->(old)
            SET old.valid_to = $ts
            """
            client.run_query(query2, {'old_id': supersedes_fact_id, 'new_id': fid, 'ts': ts})
            
        return format_result({"id": fid}, evidence="Fact remembered.")

    @mcp.tool()
    def recall(query: str, scope: str = "tenant") -> str:
        # Simplistic keyword recall. In reality, vector search.
        cypher = "MATCH (f:Fact) WHERE f.statement CONTAINS $q AND f.valid_to IS NULL RETURN f"
        res = client.run_query(cypher, {'q': query})
        return format_result(res, evidence="Facts recalled.")

    @mcp.tool()
    def session_history(session_id: str) -> str:
        cypher = "MATCH (s:Session {id: $sid})-[:HAS_MESSAGE]->(m:Message) RETURN m ORDER BY m.ts"
        res = client.run_query(cypher, {'sid': session_id})
        return format_result(res, evidence="Session history retrieved.")

    @mcp.tool()
    def find_similar_incidents(summary: str) -> str:
        cypher = "MATCH (i:Incident) WHERE i.summary CONTAINS $q RETURN i"
        res = client.run_query(cypher, {'q': summary})
        return format_result(res, evidence="Similar incidents retrieved.")

    @mcp.tool()
    def get_playbook(incident_id: str) -> str:
        cypher = "MATCH (i:Incident {id: $id})-[:RESOLVED_BY]->(p:Playbook) RETURN p"
        res = client.run_query(cypher, {'id': incident_id})
        return format_result(res, evidence="Playbook retrieved.")

    @mcp.tool()
    def record_outcome(incident_id: str, success: bool, steps: list) -> str:
        pid = str(uuid.uuid4())
        cypher = "CREATE (p:Playbook {id: $pid, steps: $steps, success_count: $sc, failure_count: $fc})"
        sc = 1 if success else 0
        fc = 0 if success else 1
        client.run_query(cypher, {'pid': pid, 'steps': json.dumps(steps), 'sc': sc, 'fc': fc})
        cypher2 = "MATCH (i:Incident {id: $id}), (p:Playbook {id: $pid}) CREATE (i)-[:RESOLVED_BY]->(p)"
        client.run_query(cypher2, {'id': incident_id, 'pid': pid})
        return format_result({"id": pid}, evidence="Outcome recorded.")
