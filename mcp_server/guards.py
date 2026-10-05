import re


def ensure_readonly(query: str):
    upper = query.upper()
    forbidden = ["CREATE", "SET", "DELETE", "REMOVE", "MERGE", "DROP", "CALL"]

    # We allow CALL algo.xxx in tools directly, but raw cypher should be read only.
    if any(re.search(r"\b" + kw + r"\b", upper) for kw in forbidden):
        raise ValueError(
            f"Read-only query guard triggered. Forbidden keywords found: {query}"
        )

    if "LIMIT" not in upper:
        query += " LIMIT 50"

    return query
