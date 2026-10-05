from pydantic import BaseModel, Field
from typing import List, Optional


class FindingVerdict(BaseModel):
    id: str
    asset: str
    cve: Optional[str] = None
    risk_score: float
    rank: int
    verdict: str = Field(..., description="act, monitor, or ignore")
    reasoning: str = Field(..., description="Justify every verdict with graph evidence")
    path: List[str] = Field(
        default_factory=list, description="Node IDs in the attack path"
    )
    sources: List[str] = Field(
        default_factory=list, description="Source spans supporting the decision"
    )
    owner: Optional[str] = None
    actions_taken: List[str] = Field(default_factory=list)
