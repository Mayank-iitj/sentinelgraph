import json
import random


def generate_company_data():
    random.seed(42)

    people = []
    teams = []
    services = []
    documents = []
    tickets = []
    chats = []
    decisions = []
    edges = []

    # 8 teams
    for i in range(8):
        teams.append({"id": f"team_{i}", "name": f"Team-{i}"})

    # 40 people
    for i in range(40):
        person = {
            "id": f"person_{i}",
            "name": f"User {i}",
            "email": f"user{i}@northwind.local",
        }
        people.append(person)
        edges.append(
            {
                "source_label": "Person",
                "source_id": person["id"],
                "target_label": "Team",
                "target_id": random.choice(teams)["id"],
                "rel_type": "MEMBER_OF",
                "properties": {},
            }
        )

    # 25 services
    for i in range(25):
        svc = {"id": f"svc_comp_{i}", "name": f"Service-{i}"}
        services.append(svc)
        edges.append(
            {
                "source_label": "Team",
                "source_id": random.choice(teams)["id"],
                "target_label": "Service",
                "target_id": svc["id"],
                "rel_type": "OWNS",
                "properties": {},
            }
        )

    # 150 docs
    for i in range(150):
        doc = {
            "id": f"doc_{i}",
            "title": f"Doc {i}",
            "path": f"/docs/{i}.md",
            "updated_at": "2026-01-01T00:00:00Z",
            "source_id": f"doc_{i}",
            "content": f"Content of doc {i}",
        }
        documents.append(doc)
        edges.append(
            {
                "source_label": "Person",
                "source_id": random.choice(people)["id"],
                "target_label": "Document",
                "target_id": doc["id"],
                "rel_type": "AUTHORED",
                "properties": {},
            }
        )

    # Planted ADR for the core demo story:
    # "the ADR that created the risky edge in the core demo story" - the internet exposed host with low CVSS to internal API
    demo_person = people[0]
    teams[0]
    planted_adr = {
        "id": "adr_demo_001",
        "title": "ADR 001: Bypass WAF for custom entry app",
        "path": "/docs/adrs/001.md",
        "updated_at": "2026-09-01T00:00:00Z",
        "source_id": "adr_demo_001",
        "content": "We decided to expose planted_entry_svc_0 directly to the internet and bypass the WAF to reduce latency for the new partner integration. It connects directly to the internal API (planted_mid_svc_0).",
    }
    documents.append(planted_adr)
    edges.append(
        {
            "source_label": "Person",
            "source_id": demo_person["id"],
            "target_label": "Document",
            "target_id": planted_adr["id"],
            "rel_type": "AUTHORED",
            "properties": {},
        }
    )

    demo_decision = {
        "id": "dec_demo_001",
        "summary": "Bypass WAF for planted_entry_svc_0",
        "rationale": "Reduce latency for partner integration",
        "date": "2026-09-01",
        "status": "active",
        "source_id": "adr_demo_001",
    }
    decisions.append(demo_decision)
    edges.append(
        {
            "source_label": "Decision",
            "source_id": demo_decision["id"],
            "target_label": "Document",
            "target_id": planted_adr["id"],
            "rel_type": "DECIDED_IN",
            "properties": {},
        }
    )

    # One decision later superseded
    dec_old = {
        "id": "dec_old_1",
        "summary": "Use RabbitMQ",
        "rationale": "Standard queue",
        "date": "2025-01-01",
        "status": "superseded",
        "source_id": "doc_old_1",
    }
    decisions.append(dec_old)
    dec_new = {
        "id": "dec_new_1",
        "summary": "Use Kafka",
        "rationale": "Need streaming",
        "date": "2026-01-01",
        "status": "active",
        "source_id": "doc_new_1",
    }
    decisions.append(dec_new)
    edges.append(
        {
            "source_label": "Decision",
            "source_id": dec_new["id"],
            "target_label": "Decision",
            "target_id": dec_old["id"],
            "rel_type": "SUPERSEDES",
            "properties": {},
        }
    )

    # Generate ground truth QA
    ground_truth_qa = [
        {
            "q": "Why is planted_entry_svc_0 exposed to the internet?",
            "a": "To reduce latency for the new partner integration.",
            "source_id": "adr_demo_001",
        },
        {
            "q": "What messaging system do we use?",
            "a": "Kafka, which superseded RabbitMQ.",
            "source_id": "doc_new_1",
        },
    ]

    data = {
        "people": people,
        "teams": teams,
        "services": services,
        "documents": documents,
        "tickets": tickets,
        "chats": chats,
        "decisions": decisions,
        "edges": edges,
        "ground_truth_qa": ground_truth_qa,
    }

    with open("data/seeds/company.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    generate_company_data()
