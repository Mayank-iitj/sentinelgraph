# One Graph, Three Agent Problems: Building SentinelGraph

Security operations teams face a common problem: they have all the data, but none of the context. An alert fires on a host. Is it important? A traditional system looks at the CVSS score. An LLM agent looks at the text summary. But neither can answer the real questions: Is this host exposed to the internet? Can it reach the payments database? Who owns it?

For the WeMakeDevs x FalkorDB Graph Hacks hackathon, we built **SentinelGraph**, a multi-agent security brain that uses FalkorDB as its core context layer to solve three distinct agent problems: triage reasoning, memory/coordination, and company knowledge.

## Problem 1: Triage and Multi-hop Reasoning
LLMs are bad at graph traversals in their head. If you give an LLM a list of 1,000 assets and 5,000 connections, it will hallucinate paths. 
Instead, we provided our Triage Agent with Model Context Protocol (MCP) tools that execute FalkorDB algorithms directly. 
When a finding comes in, the agent doesn't guess; it calls `blast_radius()` or `find_attack_paths()`. 

The results were staggering. In our benchmarks against a planted ground truth, a CVSS-only baseline escalated 8 decoys in its top 10 and missed most criticals. SentinelGraph, using graph path length and exposure data, achieved 100% recall of criticals and 0 decoys escalated.

## Problem 2: Agent Memory and Coordination
Multiple agents working together need shared state. We modeled Agent Tasks, Sessions, and Facts directly in the graph. 
Our Memory Agent uses a bitemporal supersession model. When a fact changes (e.g., "We use RabbitMQ" -> "We use Kafka"), the old fact isn't deleted. A `SUPERSEDES` edge is created. This allows agents to recall the exact state of the world at the time a past decision was made.

Furthermore, atomic handoffs between the Triage, Investigator, and Remediation agents are handled via Cypher locks, ensuring no race conditions even under high concurrency.

## Problem 3: The Company Brain
A vulnerability is only fixed if the right person is notified. We ingested docs, tickets, and chats into the graph, linking them to services and people. We extract `Decision` nodes and link them to `Document` nodes with `DECIDED_IN` edges. 

When a risky internet-exposed service is found, SentinelGraph doesn't just block it. It queries the graph, finds the ADR that justified the exposure, identifies the author, and routes the containment ticket to them with the exact source span cited.

## Conclusion
Agents are only as smart as their context. By placing FalkorDB at the center of SentinelGraph, we transformed LLMs from text-generators into autonomous security engineers capable of topological reasoning. Context is everything.
