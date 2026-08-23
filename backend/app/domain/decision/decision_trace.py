from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import datetime

@dataclass(frozen=True)
class DecisionTrace:
    """
    Central Immutable Decision Object.
    Every waste analysis MUST produce a DecisionTrace.
    Single Source of Truth for Why Not panel, Verification Queue, Waste Passport, and Audit Trail.
    """
    event_id: str
    prediction: Dict[str, Any]
    hazard: Dict[str, Any]
    evidence: Dict[str, Any]
    conflicts: Dict[str, Any]
    uncertainty: Dict[str, Any]
    risk: Dict[str, Any]
    decision: Dict[str, Any]
    counterfactual: Dict[str, Any]
    versions: Dict[str, str]
    timestamps: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
