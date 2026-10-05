from pydantic import BaseModel, Field


class FindingVerdict(BaseModel):
    id: str
    asset: str
    cve: str | None = None
    risk_score: float
    rank: int
    verdict: str = Field(..., description="act, monitor, or ignore")
    reasoning: str = Field(..., description="Justify every verdict with graph evidence")
    path: list[str] = Field(
        default_factory=list, description="Node IDs in the attack path"
    )
    sources: list[str] = Field(
        default_factory=list, description="Source spans supporting the decision"
    )
    owner: str | None = None
    actions_taken: list[str] = Field(default_factory=list)
