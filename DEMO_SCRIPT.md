# SentinelGraph Demo Script

**Total Time: 3:00 Max**

### 0:00-0:20 The CVSS Noise Problem
*Show the Triage tab, with "Counterfactual Mode" toggled ON.*
**Narration**: "Security teams are drowning in noise. When we rank findings by CVSS alone, like you see here, decoys and isolated systems bubble to the top. The real criticals—the ones with actual paths to our crown jewels—are buried. To fix this, we built SentinelGraph, placing FalkorDB at the center of an autonomous agent team."

### 0:20-1:10 Triage: Multi-hop reasoning
*Toggle "Counterfactual Mode" OFF. The findings list reorders instantly. `finding_true_0` jumps to Rank 1.*
*Click "Run Triage". The Agent Trace panel starts streaming.*
**Narration**: "When we enable the graph, our Triage Agent uses FalkorDB algorithms over MCP to calculate blast radius and shortest paths. Here it finds a low CVSS vulnerability, but FalkorDB shows it's on an internet-exposed host with a direct 4-hop path to our payments database. The decoy drops to rank 99. The agent acts on the true critical."

### 1:10-1:55 Agents & Memory
*Switch to "Agents & Memory" tab.*
**Narration**: "SentinelGraph coordinates a team of agents using the graph as a shared state layer. You can see the handoff timeline where the Triage agent claims the task atomically using a Cypher lock, then hands off to the Investigator and Remediation agents. Our Memory Agent ensures facts are superseded correctly, not overwritten. Because the graph remembers a similar cryptomining incident from last week, our agents reuse the playbook, reducing mitigation steps by 80%."

### 1:55-2:45 Company Brain
*Switch to "Company Brain" tab.*
**Narration**: "Fixing a vulnerability means finding the owner. SentinelGraph ingests documentation, tickets, and chat threads into the same graph. When I ask 'Why is this service exposed?', the brain traces the decision lineage directly to an ADR from September, citing the exact source span. It knows User 0 authored it, so the Remediation agent automatically routes the ticket to them."

### 2:45-3:00 Benchmarks & Conclusion
*Switch to "Benchmarks" tab.*
**Narration**: "Because our LLMs have tools to execute graph algorithms directly, we achieve 100% recall on planted criticals with zero decoys escalated. SentinelGraph: Context is everything."
*Display live demo URL.*
