from graph.queries import GraphClient
import uuid
import datetime


class TenancyManager:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.client = GraphClient(tenant_id)

    def init_tenant(self):
        # Create standard constraints and indices
        cypher = [
            "CREATE INDEX ON :Asset(id)",
            "CREATE INDEX ON :Identity(id)",
            "CREATE INDEX ON :AgentTask(id)",
            "CREATE INDEX ON :Session(id)",
        ]
        for c in cypher:
            try:
                self.client.run_query(c)
            except Exception:
                pass

    def get_user_session(self, user_id: str, session_id: str = None) -> str:
        if not session_id:
            session_id = str(uuid.uuid4())
            ts = datetime.datetime.now().isoformat()
            self.client.run_query(
                "CREATE (s:Session {id: $sid, user_id: $uid, created_at: $ts})",
                {"sid": session_id, "uid": user_id, "ts": ts},
            )
        return session_id

    def list_tenants(self):
        # In a real environment, we'd query redis directly for keys, but for now
        return [self.tenant_id]
