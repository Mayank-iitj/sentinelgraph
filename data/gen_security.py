import json
import random


def generate_security_data():
    random.seed(42)  # Deterministic

    assets = []
    identities = []
    services = []
    vulnerabilities = []
    alerts = []
    findings = []
    incidents = []

    edges = []  # List of dicts: {source_label, source_id, target_label, target_id, rel_type, properties}

    zones = ["DMZ", "APP", "DATA", "CORP", "CLOUD_ACCOUNTS"]

    # 1. Generate normal noise
    for i in range(400):
        zone = random.choice(zones)
        internet_exposed = zone == "DMZ"
        crown_jewel = zone == "DATA" and random.random() < 0.1

        asset = {
            "id": f"asset_{i}",
            "name": f"host-{zone.lower()}-{i}",
            "type": random.choice(["EC2", "RDS", "Container", "VM"]),
            "env": "prod" if random.random() < 0.8 else "dev",
            "internet_exposed": internet_exposed,
            "criticality": random.choice(["low", "medium", "high"]),
            "crown_jewel": crown_jewel,
        }
        assets.append(asset)

        # Service running on asset
        if random.random() < 0.8:
            svc_id = f"svc_{i}"
            services.append(
                {
                    "id": svc_id,
                    "name": random.choice(
                        ["nginx", "postgres", "node", "redis", "ssh"]
                    ),
                    "port": random.choice([80, 443, 5432, 6379, 22]),
                    "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}",
                }
            )
            edges.append(
                {
                    "source_label": "Asset",
                    "source_id": asset["id"],
                    "target_label": "Service",
                    "target_id": svc_id,
                    "rel_type": "RUNS",
                    "properties": {},
                }
            )

    for i in range(60):
        identities.append(
            {
                "id": f"id_{i}",
                "name": f"user_{i}",
                "type": random.choice(["User", "Role", "ServiceAccount"]),
                "privileged": random.random() < 0.2,
            }
        )

    for i in range(800):
        cvss = round(random.uniform(2.0, 9.8), 1)
        vulnerabilities.append(
            {
                "id": f"vuln_{i}",
                "cve": f"CVE-2026-{10000 + i}",
                "cvss": cvss,
                "epss": round(random.uniform(0.01, 0.9), 3),
                "exploit_available": random.random() < (0.8 if cvss > 8.0 else 0.1),
            }
        )

        # Attach to random service
        svc = random.choice(services)
        edges.append(
            {
                "source_label": "Service",
                "source_id": svc["id"],
                "target_label": "Vulnerability",
                "target_id": f"vuln_{i}",
                "rel_type": "AFFECTED_BY",
                "properties": {},
            }
        )

    for i in range(300):
        alerts.append(
            {
                "id": f"alert_{i}",
                "source": random.choice(["GuardDuty", "CrowdStrike", "WAF", "Custom"]),
                "severity": random.choice(["LOW", "MEDIUM", "HIGH"]),
                "ts": 1696000000 + i * 1000,
                "summary": f"Suspicious activity {i}",
            }
        )
        # Randomly trigger on asset
        a = random.choice(assets)
        edges.append(
            {
                "source_label": "Alert",
                "source_id": f"alert_{i}",
                "target_label": "Asset",
                "target_id": a["id"],
                "rel_type": "TRIGGERED_ON",
                "properties": {},
            }
        )

    # Now we plant ground truth

    # 8 true criticals: low/medium CVSS, internet-reachable, 3-6 hop path to crown jewel
    # Path: Asset(internet) -RUNS-> Service -AFFECTED_BY-> Vuln (Finding)
    # Service -CONNECTS_TO-> Asset(internal) -HAS_ACCESS-> Identity -CAN_ASSUME-> Identity(priv) -HAS_ACCESS-> Asset(crown jewel)
    crown_jewels = [a for a in assets if a["crown_jewel"]]

    for i in range(8):
        cj = random.choice(crown_jewels)
        # Create internet exposed asset
        entry_asset = {
            "id": f"planted_entry_asset_{i}",
            "name": f"exposed-entry-{i}",
            "type": "EC2",
            "env": "prod",
            "internet_exposed": True,
            "criticality": "high",
            "crown_jewel": False,
        }
        assets.append(entry_asset)

        # Create service on entry
        entry_svc = {
            "id": f"planted_entry_svc_{i}",
            "name": "custom-app",
            "port": 8080,
            "version": "1.0",
        }
        services.append(entry_svc)
        edges.append(
            {
                "source_label": "Asset",
                "source_id": entry_asset["id"],
                "target_label": "Service",
                "target_id": entry_svc["id"],
                "rel_type": "RUNS",
                "properties": {},
            }
        )

        # Low CVSS vuln
        planted_vuln = {
            "id": f"planted_vuln_{i}",
            "cve": f"CVE-2026-PLANT{i}",
            "cvss": 4.5,
            "epss": 0.8,
            "exploit_available": True,
        }
        vulnerabilities.append(planted_vuln)
        edges.append(
            {
                "source_label": "Service",
                "source_id": entry_svc["id"],
                "target_label": "Vulnerability",
                "target_id": planted_vuln["id"],
                "rel_type": "AFFECTED_BY",
                "properties": {},
            }
        )

        # Finding for this vuln
        finding = {"id": f"finding_true_{i}", "status": "open", "risk_score": 0.0}
        findings.append(finding)
        edges.append(
            {
                "source_label": "Finding",
                "source_id": finding["id"],
                "target_label": "Vulnerability",
                "target_id": planted_vuln["id"],
                "rel_type": "ABOUT",
                "properties": {},
            }
        )
        edges.append(
            {
                "source_label": "Finding",
                "source_id": finding["id"],
                "target_label": "Asset",
                "target_id": entry_asset["id"],
                "rel_type": "AFFECTS",
                "properties": {},
            }
        )

        # Path construction (4 hops to cj)
        mid_asset = {
            "id": f"planted_mid_asset_{i}",
            "name": f"internal-hop-{i}",
            "type": "VM",
            "env": "prod",
            "internet_exposed": False,
            "criticality": "medium",
            "crown_jewel": False,
        }
        assets.append(mid_asset)

        mid_svc = {
            "id": f"planted_mid_svc_{i}",
            "name": "internal-api",
            "port": 9000,
            "version": "1.0",
        }
        services.append(mid_svc)
        edges.append(
            {
                "source_label": "Asset",
                "source_id": mid_asset["id"],
                "target_label": "Service",
                "target_id": mid_svc["id"],
                "rel_type": "RUNS",
                "properties": {},
            }
        )

        edges.append(
            {
                "source_label": "Service",
                "source_id": entry_svc["id"],
                "target_label": "Service",
                "target_id": mid_svc["id"],
                "rel_type": "CONNECTS_TO",
                "properties": {"port": 9000, "protocol": "tcp"},
            }
        )

        mid_role = {
            "id": f"planted_mid_role_{i}",
            "name": f"role-{i}",
            "type": "Role",
            "privileged": False,
        }
        identities.append(mid_role)
        edges.append(
            {
                "source_label": "Asset",
                "source_id": mid_asset["id"],
                "target_label": "Identity",
                "target_id": mid_role["id"],
                "rel_type": "CAN_ASSUME",
                "properties": {},
            }
        )

        edges.append(
            {
                "source_label": "Identity",
                "source_id": mid_role["id"],
                "target_label": "Asset",
                "target_id": cj["id"],
                "rel_type": "HAS_ACCESS",
                "properties": {"level": "admin"},
            }
        )

    # 15 decoys (CVSS 9+, isolated)
    for i in range(15):
        decoy_asset = {
            "id": f"planted_decoy_asset_{i}",
            "name": f"isolated-dev-{i}",
            "type": "VM",
            "env": "dev",
            "internet_exposed": False,
            "criticality": "low",
            "crown_jewel": False,
        }
        assets.append(decoy_asset)
        decoy_svc = {
            "id": f"planted_decoy_svc_{i}",
            "name": "test-app",
            "port": 80,
            "version": "0.1",
        }
        services.append(decoy_svc)
        edges.append(
            {
                "source_label": "Asset",
                "source_id": decoy_asset["id"],
                "target_label": "Service",
                "target_id": decoy_svc["id"],
                "rel_type": "RUNS",
                "properties": {},
            }
        )

        decoy_vuln = {
            "id": f"planted_decoy_vuln_{i}",
            "cve": f"CVE-2026-DECOY{i}",
            "cvss": 9.9,
            "epss": 0.05,
            "exploit_available": False,
        }
        vulnerabilities.append(decoy_vuln)
        edges.append(
            {
                "source_label": "Service",
                "source_id": decoy_svc["id"],
                "target_label": "Vulnerability",
                "target_id": decoy_vuln["id"],
                "rel_type": "AFFECTED_BY",
                "properties": {},
            }
        )

        finding = {"id": f"finding_decoy_{i}", "status": "open", "risk_score": 0.0}
        findings.append(finding)
        edges.append(
            {
                "source_label": "Finding",
                "source_id": finding["id"],
                "target_label": "Vulnerability",
                "target_id": decoy_vuln["id"],
                "rel_type": "ABOUT",
                "properties": {},
            }
        )
        edges.append(
            {
                "source_label": "Finding",
                "source_id": finding["id"],
                "target_label": "Asset",
                "target_id": decoy_asset["id"],
                "rel_type": "AFFECTS",
                "properties": {},
            }
        )

    # 1 Multi-stage incident (6 alerts, 4 assets)
    inc_assets = [
        {
            "id": f"inc_asset_{j}",
            "name": f"inc-host-{j}",
            "type": "EC2",
            "env": "prod",
            "internet_exposed": (j == 0),
            "criticality": "high",
            "crown_jewel": (j == 3),
        }
        for j in range(4)
    ]
    assets.extend(inc_assets)
    for j in range(3):
        edges.append(
            {
                "source_label": "Asset",
                "source_id": inc_assets[j]["id"],
                "target_label": "Asset",
                "target_id": inc_assets[j + 1]["id"],
                "rel_type": "CONNECTS_TO",
                "properties": {"port": 22, "protocol": "ssh"},
            }
        )

    multi_incident = {
        "id": "incident_multistage",
        "status": "open",
        "summary": "Multi-stage attack",
    }
    incidents.append(multi_incident)
    for j in range(6):
        a_id = f"inc_alert_{j}"
        alerts.append(
            {
                "id": a_id,
                "source": "Custom",
                "severity": "HIGH",
                "ts": 1696000000 + j * 60,
                "summary": f"Stage {j}",
            }
        )
        edges.append(
            {
                "source_label": "Incident",
                "source_id": multi_incident["id"],
                "target_label": "Alert",
                "target_id": a_id,
                "rel_type": "INVOLVES",
                "properties": {},
            }
        )
        edges.append(
            {
                "source_label": "Alert",
                "source_id": a_id,
                "target_label": "Asset",
                "target_id": inc_assets[j % 4]["id"],
                "rel_type": "TRIGGERED_ON",
                "properties": {},
            }
        )

    # Lateral movement story CAN_ASSUME chaining
    lat_roles = [
        {
            "id": f"lat_role_{j}",
            "name": f"lat-role-{j}",
            "type": "Role",
            "privileged": False,
        }
        for j in range(4)
    ]
    identities.extend(lat_roles)
    for j in range(3):
        edges.append(
            {
                "source_label": "Identity",
                "source_id": lat_roles[j]["id"],
                "target_label": "Identity",
                "target_id": lat_roles[j + 1]["id"],
                "rel_type": "CAN_ASSUME",
                "properties": {},
            }
        )
    edges.append(
        {
            "source_label": "Identity",
            "source_id": lat_roles[-1]["id"],
            "target_label": "Asset",
            "target_id": crown_jewels[0]["id"],
            "rel_type": "HAS_ACCESS",
            "properties": {"level": "admin"},
        }
    )

    # 2 Repeat pattern incidents for playbook reuse
    for i in range(2):
        repeat_inc = {
            "id": f"incident_repeat_{i}",
            "status": "open",
            "summary": "Cryptomining pattern",
        }
        incidents.append(repeat_inc)
        rep_alert = {
            "id": f"rep_alert_{i}",
            "source": "GuardDuty",
            "severity": "HIGH",
            "ts": 1696000000 + i * 86400,
            "summary": "Cryptomining domain connection",
        }
        alerts.append(rep_alert)
        edges.append(
            {
                "source_label": "Incident",
                "source_id": repeat_inc["id"],
                "target_label": "Alert",
                "target_id": rep_alert["id"],
                "rel_type": "INVOLVES",
                "properties": {},
            }
        )
        edges.append(
            {
                "source_label": "Alert",
                "source_id": rep_alert["id"],
                "target_label": "Asset",
                "target_id": assets[i]["id"],
                "rel_type": "TRIGGERED_ON",
                "properties": {},
            }
        )

    data = {
        "assets": assets,
        "identities": identities,
        "services": services,
        "vulnerabilities": vulnerabilities,
        "alerts": alerts,
        "findings": findings,
        "incidents": incidents,
        "edges": edges,
    }

    with open("data/seeds/security.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    generate_security_data()
