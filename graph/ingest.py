import os
import json
from falkordb import FalkorDB


def ingest_data(tenant_id: str = "tenant_1"):
    """Ingest seed data into FalkorDB graph. Fully synchronous."""
    db_url = os.getenv("FALKORDB_URL", "redis://localhost:6379")
    db = FalkorDB.from_url(db_url)
    graph = db.select_graph(tenant_id)

    print(f"Ingesting into graph: {tenant_id}")

    # Load schema
    with open("graph/schema.cypher") as f:
        schema_cypher = f.read()

    # Apply schema line by line
    for line in schema_cypher.split(";"):
        line = line.strip()
        if line and not line.startswith("//"):
            try:
                graph.query(line)
            except Exception as e:  # noqa: BLE001 - duplicate schema is non-fatal
                print(f"Schema ignore (likely already exists): {e}")

    # Load data
    with open("data/seeds/security.json") as f:
        security_data = json.load(f)

    with open("data/seeds/company.json") as f:
        company_data = json.load(f)

    # We will use UNWIND for bulk insert
    def insert_nodes(label, items):
        if not items:
            return
        query = f"UNWIND $items AS item CREATE (n:{label}) SET n = item"
        graph.query(query, {"items": items})
        print(f"  Inserted {len(items)} {label} nodes")

    print("Inserting security nodes...")
    insert_nodes("Asset", security_data.get("assets", []))
    insert_nodes("Identity", security_data.get("identities", []))
    insert_nodes("Service", security_data.get("services", []))
    insert_nodes("Vulnerability", security_data.get("vulnerabilities", []))
    insert_nodes("Alert", security_data.get("alerts", []))
    insert_nodes("Finding", security_data.get("findings", []))
    insert_nodes("Incident", security_data.get("incidents", []))

    print("Inserting company nodes...")
    insert_nodes("Person", company_data.get("people", []))
    insert_nodes("Team", company_data.get("teams", []))
    insert_nodes("Document", company_data.get("documents", []))
    insert_nodes("Decision", company_data.get("decisions", []))
    insert_nodes("Service", company_data.get("services", []))

    print("Inserting edges...")
    all_edges = security_data.get("edges", []) + company_data.get("edges", [])

    # Group edges by rel_type and src_label/tgt_label
    edges_by_type = {}
    for edge in all_edges:
        key = (edge["source_label"], edge["target_label"], edge["rel_type"])
        if key not in edges_by_type:
            edges_by_type[key] = []
        edges_by_type[key].append(
            {
                "source_id": edge["source_id"],
                "target_id": edge["target_id"],
                "properties": edge.get("properties", {}),
            }
        )

    for (src_label, tgt_label, rel_type), edges_list in edges_by_type.items():
        query = f"""
        UNWIND $edges AS edge 
        MATCH (s:{src_label} {{id: edge.source_id}}), (t:{tgt_label} {{id: edge.target_id}}) 
        CREATE (s)-[r:{rel_type}]->(t) 
        SET r = edge.properties
        """
        try:
            graph.query(query, {"edges": edges_list})
            print(
                f"  Inserted {len(edges_list)} {src_label}-[{rel_type}]->{tgt_label} edges"
            )
        except Exception as e:  # noqa: BLE001 - duplicate edge is non-fatal
            print(f"  Warning: Edge insert {rel_type} failed: {e}")

    print("Ingestion complete!")


if __name__ == "__main__":
    ingest_data()
