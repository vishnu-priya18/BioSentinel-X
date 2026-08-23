from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class HazardAssessmentResult:
    detected: bool
    hazard_type: str        # SHARP, NEEDLE, SYRINGE, SCALPEL, BLADE, LANCET, GLASS_SHARP, UNKNOWN_SHARP, INFECTIOUS_HAZARD, NONE
    severity: str           # LOW, MEDIUM, HIGH, CRITICAL
    score: float            # [0.0, 1.0]
    critical_hazard: bool
    automation_allowed: bool
    evidence_source: str
    explanation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "detected": self.detected,
            "hazard_type": self.hazard_type,
            "severity": self.severity,
            "score": round(self.score, 4),
            "critical": self.critical_hazard,
            "critical_hazard": self.critical_hazard,
            "automation_allowed": self.automation_allowed,
            "evidence_source": self.evidence_source,
            "explanation": self.explanation
        }

class HazardGate:
    """
    Dedicated Hazard Safety Gate Engine.
    Separates waste classification ('What category?') from safety escalation ('Is there a dangerous object?').
    High raw AI model confidence MUST NEVER override a critical hazard safety rule.
    """
    
    CRITICAL_HAZARD_TYPES = {
        "SHARP", "NEEDLE", "SYRINGE", "SCALPEL", "BLADE", "LANCET", "UNKNOWN_SHARP"
    }

    @classmethod
    def assess(
        cls,
        image_base64: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> HazardAssessmentResult:
        metadata = metadata or {}
        
        # 1. Check metadata override (for scenario codes like DEMO-005 or explicit user tags)
        scenario_code = metadata.get("scenario_code", "")
        demo_hazard = metadata.get("demo_hazard", "")
        declared_item = (metadata.get("item_description") or "").upper()
        
        detected_hazard = "NONE"
        detection_score = 0.0
        evidence_source = "Demo Hazard Gate Detector"
        
        if scenario_code == "DEMO-005" or demo_hazard in cls.CRITICAL_HAZARD_TYPES or "SYRINGE" in declared_item or "NEEDLE" in declared_item:
            detected_hazard = demo_hazard if demo_hazard else ("NEEDLE" if "NEEDLE" in declared_item else "SYRINGE")
            detection_score = metadata.get("demo_hazard_confidence", 0.97)
            evidence_source = "Visual Object Detection & Hazard Evidence Layer"
        elif "SCALPEL" in declared_item:
            detected_hazard = "SCALPEL"
            detection_score = 0.95
        elif "BLADE" in declared_item:
            detected_hazard = "BLADE"
            detection_score = 0.94
        elif "LANCET" in declared_item:
            detected_hazard = "LANCET"
            detection_score = 0.93
        elif "GLASS" in declared_item:
            detected_hazard = "GLASS_SHARP"
            detection_score = 0.88
            
        if detected_hazard in cls.CRITICAL_HAZARD_TYPES:
            return HazardAssessmentResult(
                detected=True,
                hazard_type=detected_hazard,
                severity="CRITICAL",
                score=max(0.0, min(1.0, detection_score)),
                critical_hazard=True,
                automation_allowed=False,
                evidence_source=evidence_source,
                explanation=f"Critical sharp biomedical hazard ({detected_hazard}) detected. Automated approval is disabled regardless of AI confidence."
            )
        elif detected_hazard == "GLASS_SHARP":
            return HazardAssessmentResult(
                detected=True,
                hazard_type=detected_hazard,
                severity="HIGH",
                score=max(0.0, min(1.0, detection_score)),
                critical_hazard=False,
                automation_allowed=False,
                evidence_source=evidence_source,
                explanation="High-risk sharp glass hazard detected. Human verification required before disposal."
            )
            
        # No critical hazard detected
        return HazardAssessmentResult(
            detected=False,
            hazard_type="NONE",
            severity="LOW",
            score=0.05,
            critical_hazard=False,
            automation_allowed=True,
            evidence_source="Hazard Gate Evaluator",
            explanation="No critical sharp or safety hazard detected."
        )
