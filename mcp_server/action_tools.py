from mcp.server.fastmcp import FastMCP
import json
import uuid

def format_result(data, evidence="", path=[]):
    return json.dumps({"result": data, "evidence": evidence, "path": path})

action_log = []

def register_action_tools(mcp: FastMCP):
    
    @mcp.tool()
    def create_ticket(title: str, description: str, assignee_id: str = None, dry_run: bool = False) -> str:
        tid = str(uuid.uuid4())
        ticket = {"id": tid, "title": title, "description": description, "assignee": assignee_id}
        if dry_run:
            return format_result(ticket, evidence="[DRY RUN] Ticket would be created.")
            
        action_log.append({"action": "create_ticket", "data": ticket})
        return format_result(ticket, evidence="Ticket created.")

    @mcp.tool()
    def draft_containment(incident_id: str, steps: list, dry_run: bool = False) -> str:
        if dry_run:
            return format_result({"incident_id": incident_id, "steps": steps}, evidence="[DRY RUN] Containment playbook drafted.")
            
        action_log.append({"action": "draft_containment", "incident_id": incident_id, "steps": steps})
        return format_result({"incident_id": incident_id}, evidence="Containment playbook drafted.")

    @mcp.tool()
    def escalate(finding_id: str, reason: str, dry_run: bool = False) -> str:
        if dry_run:
            return format_result({"finding": finding_id, "reason": reason}, evidence="[DRY RUN] Finding would be escalated.")
            
        action_log.append({"action": "escalate", "finding_id": finding_id, "reason": reason})
        return format_result({"finding_id": finding_id}, evidence="Finding escalated.")

    @mcp.tool()
    def assign(task_id: str, user_id: str, dry_run: bool = False) -> str:
        if dry_run:
            return format_result({"task": task_id, "user": user_id}, evidence="[DRY RUN] Task would be assigned.")
            
        action_log.append({"action": "assign", "task_id": task_id, "user_id": user_id})
        return format_result({"task_id": task_id}, evidence="Task assigned.")
