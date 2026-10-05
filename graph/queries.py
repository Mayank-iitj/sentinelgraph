from typing import List, Dict, Any

class GraphClient:
    def __init__(self, tenant_id: str = "tenant_1"):
        import os
        db_url = os.getenv("FALKORDB_URL", "redis://localhost:6379")
        if os.getenv("MOCK_GRAPH") == "1":
            self.graph = None
            return
            
        try:
            from falkordb import FalkorDB
            # Add timeout so it fails fast instead of hanging if Docker is down
            self.db = FalkorDB.from_url(db_url, socket_timeout=2, socket_connect_timeout=2)
            self.graph = self.db.select_graph(tenant_id)
        except Exception:
            self.graph = None # For offline testing

    def run_query(self, query: str, params: dict = None) -> List[List[Any]]:
        if self.graph:
            res = self.graph.query(query, params or {})
            return res.result_set
        return []

    def run_query_readonly(self, query: str, params: dict = None) -> List[List[Any]]:
        upper_query = query.upper()
        forbidden = ["CREATE", "SET", "DELETE", "REMOVE", "MERGE", "DROP", "CALL"]
        if any(keyword in upper_query for keyword in forbidden):
            raise ValueError(f"Read-only query cannot contain mutation keywords.")
        
        # Enforce limit
        if "LIMIT" not in upper_query:
            query += " LIMIT 100"
            
        return self.run_query(query, params)

    def find_attack_paths(self, source_filter: str, target_id: str, max_hops: int = 5, limit: int = 10):
        # Cypher shortest path
        # source_filter like 'a:Asset {internet_exposed: true}'
        query = f"""
        MATCH p = shortestPath(({source_filter})-[*1..{max_hops}]->(t:Asset {{id: $target_id}}))
        RETURN p
        LIMIT $limit
        """
        return self.run_query(query, {'target_id': target_id, 'limit': limit})
        
    def get_asset_context(self, asset_id: str):
        query = """
        MATCH (a:Asset {id: $asset_id})-[r]-(connected)
        RETURN a, type(r), connected
        """
        return self.run_query(query, {'asset_id': asset_id})
        
    def get_vulns_for_asset(self, asset_id: str):
        query = """
        MATCH (a:Asset {id: $asset_id})-[:RUNS]->(s:Service)-[:AFFECTED_BY]->(v:Vulnerability)
        RETURN v
        """
        return self.run_query(query, {'asset_id': asset_id})
