import datetime
import logging
import uuid
from graph.queries import GraphClient

logger = logging.getLogger(__name__)


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
            except (RuntimeError, ValueError) as exc:
                logger.debug(
                    "Tenant constraint may already exist",
                    extra={"constraint": c, "error": str(exc)},
                )
            except Exception as exc:  # noqa: BLE001 - duplicate schema is non-fatal
                logger.debug("Tenant constraint skipped: %s", exc)

    def get_user_session(self, user_id: str, session_id: str | None = None) -> str:
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
