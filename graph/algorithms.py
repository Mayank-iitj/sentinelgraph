from .queries import GraphClient
import networkx as nx


class GraphAlgorithms:
    def __init__(self, client: GraphClient):
        self.client = client

    def _fetch_subgraph(self):
        # Fallback subgraph fetch for NetworkX
        query = "MATCH (n)-[r]->(m) RETURN id(n), id(m), labels(n), type(r)"
        results = self.client.run_query(query)
        G = nx.DiGraph()
        for row in results:
            if not row:
                continue
            u, v, _l_u, r_type = row[0], row[1], row[2], row[3]
            G.add_edge(u, v, type=r_type)
        return G

    def blast_radius(self, asset_id: str, max_hops: int = 3):
        # Finds everything reachable from asset_id within max_hops
        query = f"""
        MATCH (a:Asset {{id: $asset_id}})-[*1..{max_hops}]->(connected)
        RETURN DISTINCT connected
        """
        return self.client.run_query(query, {"asset_id": asset_id})

    def rank_by_centrality(self, metric: str = "pagerank"):
        try:
            if metric == "pagerank":
                query = "CALL algo.pageRank('Asset')"
                return self.client.run_query(query)
            elif metric == "betweenness":
                query = "CALL algo.betweenness('Asset')"
                return self.client.run_query(query)
            elif metric == "degree":
                query = "CALL algo.degreeCentrality('Asset')"
                return self.client.run_query(query)
        except Exception:
            # Fallback to networkx
            G = self._fetch_subgraph()
            if not G.nodes:
                return []
            if metric == "pagerank":
                scores = nx.pagerank(G)
            elif metric == "betweenness":
                scores = nx.betweenness_centrality(G)
            elif metric == "degree":
                scores = nx.degree_centrality(G)
            else:
                scores = {}
            # Sort by score
            return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def cluster_alerts(self):
        try:
            query = "CALL algo.wcc('Alert', 'TRIGGERED_ON')"
            return self.client.run_query(query)
        except Exception:
            # Fallback to wcc on undirected nx
            G = self._fetch_subgraph().to_undirected()
            components = list(nx.connected_components(G))
            return components
