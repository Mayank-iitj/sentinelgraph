import pytest
from graph.queries import GraphClient
from graph.algorithms import GraphAlgorithms
from mcp_server.guards import ensure_readonly
from memory.semantic import SemanticMemory
from memory.procedural import ProceduralMemory
from memory.episodic import EpisodicMemory
from brain.extract import BrainExtractor
from brain.ingest import BrainIngestor
from brain.provenance import ProvenanceTracker

# ──────── Guard Tests ────────

def test_ensure_readonly_appends_limit():
    safe_query = "MATCH (n) RETURN n"
    assert ensure_readonly(safe_query) == safe_query + " LIMIT 50"

def test_ensure_readonly_blocks_set():
    with pytest.raises(ValueError):
        ensure_readonly("MATCH (n) SET n.prop = 1")

def test_ensure_readonly_blocks_create():
    with pytest.raises(ValueError):
        ensure_readonly("CREATE (n:Test)")

def test_ensure_readonly_blocks_delete():
    with pytest.raises(ValueError):
        ensure_readonly("MATCH (n) DELETE n")

def test_ensure_readonly_blocks_merge():
    with pytest.raises(ValueError):
        ensure_readonly("MERGE (n:Test {id: 1})")

def test_ensure_readonly_preserves_existing_limit():
    query = "MATCH (n) RETURN n LIMIT 10"
    assert ensure_readonly(query) == query  # should NOT double-add LIMIT

# ──────── GraphClient Offline Tests ────────

def test_graph_client_offline():
    client = GraphClient()
    assert client.run_query("MATCH (n) RETURN n") == []

def test_graph_client_readonly_offline():
    client = GraphClient()
    assert client.run_query_readonly("MATCH (n) RETURN n") == []

def test_graph_client_readonly_rejects_mutations():
    client = GraphClient()
    with pytest.raises(ValueError):
        client.run_query_readonly("CREATE (n:Test)")

def test_graph_client_attack_paths_offline():
    client = GraphClient()
    result = client.find_attack_paths("a:Asset", "target_1")
    assert result == []

def test_graph_client_asset_context_offline():
    client = GraphClient()
    result = client.get_asset_context("asset_1")
    assert result == []

# ──────── Algorithm Tests (Offline) ────────

def test_algorithms_blast_radius_offline():
    client = GraphClient()
    algo = GraphAlgorithms(client)
    result = algo.blast_radius("asset_1")
    assert result == []

# ──────── Memory Module Tests (Offline) ────────

def test_semantic_memory_init():
    mem = SemanticMemory()
    assert mem.client is not None

def test_procedural_memory_init():
    mem = ProceduralMemory()
    assert mem.client is not None

def test_episodic_memory_init():
    mem = EpisodicMemory()
    assert mem.client is not None

# ──────── Brain Module Tests (Offline) ────────

def test_brain_extractor_offline():
    extractor = BrainExtractor()
    decisions = extractor.extract_decisions("doc_1", "some content")
    assert len(decisions) == 1
    assert decisions[0]["id"] == "stub_dec"

def test_brain_ingestor_init():
    ingestor = BrainIngestor()
    assert ingestor.client is not None

def test_provenance_tracker_init():
    tracker = ProvenanceTracker()
    assert tracker.client is not None
