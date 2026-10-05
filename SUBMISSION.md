# Graph Hacks Submission: SentinelGraph

**Project Name:** SentinelGraph
**Repo URL:** https://github.com/Mayank-iitj/sentinelgraph
**Live Demo URL:** https://sentinelgraph.demo.app
**Video URL:** https://youtube.com/watch?v=demo
**Blog URL:** https://dev.to/mayank/sentinelgraph

**Tracks Entered:**
- T1: Agents That Act on Connected Data (Primary)
- T2: Agent Memory and Coordination
- T3: Company Brain

**Tech Stack Used:**
FalkorDB, Python, FastAPI, Anthropic API, Model Context Protocol (MCP), React, Vite, Cytoscape.js.

**3-Line Pitch:**
SentinelGraph is a multi-agent security operations brain built on FalkorDB. It uses graph algorithms via MCP to accurately triage vulnerabilities based on blast radius rather than just CVSS. It remembers past incidents to reuse playbooks and routes containment tickets to the exact developer who introduced the risk, citing the original architecture decision.

**150-Word Description:**
SentinelGraph transforms noisy security alerts into actionable intelligence using FalkorDB as its core context layer. Traditional triage relies on CVSS, resulting in high-severity decoys burying low-severity criticals. SentinelGraph solves this by giving LLM agents MCP tools to execute graph algorithms (shortest path, pagerank) directly against the infrastructure graph, enabling topological reasoning. 

Beyond triage, SentinelGraph solves agent memory and company knowledge. A bitemporal memory graph handles fact supersession and playbook reuse for repeat incidents. A "Company Brain" subgraph links services to their owners and the historical architecture decisions (ADRs) that created them. When SentinelGraph mitigates a threat, it doesn't just block an IP—it finds the developer who made the service internet-exposed, cites their design doc, and assigns them a containment ticket with a drafted playbook. Context is everything.

## Track Mapping
### T1: Agents That Act on Connected Data
- **Multi-hop reasoning:** `mcp_server/graph_tools.py` (`find_attack_paths`)
- **Algorithms as tools:** `mcp_server/graph_tools.py` (`blast_radius`, `rank_by_centrality`)
- **Actions based on graph:** `agents/triage.py` relies on `risk_score` over graph paths.

### T2: Agent Memory and Coordination
- **Memory supersession:** `mcp_server/memory_tools.py` (`remember_fact` with `SUPERSEDES` edge)
- **Playbook reuse:** `mcp_server/memory_tools.py` (`get_playbook`, `record_outcome`)
- **Handoffs:** Displayed in the Agents & Memory UI tab.

### T3: Company Brain
- **Knowledge provenance:** `data/gen_company.py` plants ADRs; `mcp_server/brain_tools.py` (`trace_decision`)
- **Owner routing:** `mcp_server/brain_tools.py` (`route_to_owner`)
