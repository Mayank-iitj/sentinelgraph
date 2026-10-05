from mcp.server.fastmcp import FastMCP
from graph.queries import GraphClient
from graph.algorithms import GraphAlgorithms
from mcp_server.guards import ensure_readonly
import json


def format_result(data, evidence="", path=[]):
    return json.dumps({"result": data, "evidence": evidence, "path": path})


def register_graph_tools(mcp: FastMCP):
    client = GraphClient()
    algo = GraphAlgorithms(client)

    @mcp.tool()
    def find_attack_paths(
        source_filter: str, target: str, max_hops: int = 5, limit: int = 10
    ) -> str:
        res = client.find_attack_paths(source_filter, target, max_hops, limit)
        return format_result(res, evidence=f"Found {len(res)} paths.", path=res)

    @mcp.tool()
    def blast_radius(asset_id: str, max_hops: int = 3) -> str:
        res = algo.blast_radius(asset_id, max_hops)
        return format_result(res, evidence=f"Blast radius affects {len(res)} nodes.")

    @mcp.tool()
    def rank_by_centrality(metric: str = "pagerank") -> str:
        res = algo.rank_by_centrality(metric)
        return format_result(res, evidence=f"Ranked {len(res)} nodes by {metric}.")

    @mcp.tool()
    def cluster_alerts() -> str:
        res = algo.cluster_alerts()
        return format_result(res, evidence=f"Found {len(res)} clusters.")

    @mcp.tool()
    def identity_reach(identity_id: str) -> str:
        query = "MATCH (i:Identity {id: $id})-[:CAN_ASSUME*0..3]->(role:Identity)-[:HAS_ACCESS]->(a:Asset) RETURN a"
        res = client.run_query(query, {"id": identity_id})
        return format_result(res, evidence=f"Identity can reach {len(res)} assets.")

    @mcp.tool()
    def get_asset_context(asset_id: str) -> str:
        res = client.get_asset_context(asset_id)
        return format_result(res, evidence=f"Context for asset {asset_id}.")

    @mcp.tool()
    def get_vulns_for_asset(asset_id: str) -> str:
        res = client.get_vulns_for_asset(asset_id)
        return format_result(res, evidence=f"Vulns for {asset_id}.")

    @mcp.tool()
    def risk_score(finding_id: str) -> str:
        # returns component breakdown (CVSS, EPSS, exploit, exposure reachability, path length to crown jewel, centrality)
        query = """
        MATCH (f:Finding {id: $fid})-[:ABOUT]->(v:Vulnerability)
        MATCH (f)-[:AFFECTS]->(a:Asset)
        OPTIONAL MATCH p = shortestPath((a)-[*1..5]->(cj:Asset {crown_jewel: true}))
        RETURN v.cvss, v.epss, v.exploit_available, a.internet_exposed, length(p)
        """
        res = client.run_query(query, {"fid": finding_id})

        if not res:
            return format_result({}, evidence="Finding not found.")

        cvss, epss, exploit, exposed, path_len = res[0]
        score = (cvss or 0.0) * 0.1
        if exploit:
            score += 2.0
        if exposed:
            score += 3.0
        if path_len is not None:
            score += max(0, (5 - path_len)) * 1.5

        breakdown = {
            "risk_score": score,
            "CVSS": cvss,
            "EPSS": epss,
            "exploit_available": exploit,
            "exposure": exposed,
            "path_length_to_crown_jewel": path_len,
        }
        return format_result(breakdown, evidence="Risk score calculated.")

    @mcp.tool()
    def run_cypher_readonly(query: str) -> str:
        safe_query = ensure_readonly(query)
        res = client.run_query(safe_query)
        return format_result(res, evidence="Executed read-only cypher.")
