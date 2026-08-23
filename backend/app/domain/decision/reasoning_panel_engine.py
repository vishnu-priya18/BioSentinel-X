from typing import List, Dict, Any, Optional

class ReasoningPanelEngine:
    """
    Generates structured human-readable reasons for the 'Why Not?' UI panel.
    Statuses: PASS, WARNING, FAIL.
    Separates raw AI confidence from operational safety permission.
    """
    @staticmethod
    def generate_reasons(
        quality_score: float,
        confidence: float,
        observability: str,
        conflict_codes: List[str],
        uncertainty_score: float,
        z_score: float,
        hazard_result: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        items = []
        
        # 1. Image Quality
        if quality_score >= 0.70:
            items.append({
                "status": "PASS",
                "source": "Image Quality",
                "message": "Visual evidence quality is clear and sufficient.",
                "technical_value": f"{quality_score:.2f}",
                "explanation": "Image clarity meets threshold requirements for edge features."
            })
        else:
            items.append({
                "status": "FAIL",
                "source": "Image Quality",
                "message": "Visual evidence quality is too low or blurry.",
                "technical_value": f"{quality_score:.2f}",
                "explanation": "Image blur or low resolution prevents trustworthy visual classification."
            })
            
        # 2. Raw AI Confidence
        items.append({
            "status": "PASS" if confidence >= 0.80 else "WARNING",
            "source": "AI Confidence",
            "message": f"Model prediction confidence is {confidence * 100:.1f}%.",
            "technical_value": f"{confidence:.2f}",
            "explanation": "Raw model confidence describes prediction probability, NOT operational safety permission."
        })
        
        # 3. Critical Hazard Gate Evaluation
        if hazard_result and hazard_result.detected:
            if hazard_result.critical_hazard:
                items.append({
                    "status": "FAIL",
                    "source": "Critical Hazard Gate",
                    "message": f"Critical sharp hazard detected ({hazard_result.hazard_type}).",
                    "technical_value": hazard_result.hazard_type,
                    "explanation": "Automated approval is disabled regardless of AI confidence whenever a critical sharp is detected."
                })
                items.append({
                    "status": "FAIL",
                    "source": "Automation Permission",
                    "message": "Automated processing BLOCKED by safety policy.",
                    "technical_value": "BLOCKED",
                    "explanation": "High AI confidence does not override a safety-critical hazard rule."
                })
            else:
                items.append({
                    "status": "WARNING",
                    "source": "Hazard Gate",
                    "message": f"Potential hazard detected ({hazard_result.hazard_type}).",
                    "technical_value": hazard_result.hazard_type,
                    "explanation": "Requires safety verification before automated disposal."
                })
        else:
            items.append({
                "status": "PASS",
                "source": "Hazard Gate",
                "message": "No critical sharp biomedical hazard detected.",
                "technical_value": "NONE",
                "explanation": "Visual and evidence layers report no prohibited sharp objects."
            })
        
        # 4. Observability
        if observability == "NOT_OBSERVABLE":
            items.append({
                "status": "FAIL",
                "source": "Observability",
                "message": "Container contents are not directly observable.",
                "technical_value": "NOT_OBSERVABLE",
                "explanation": "Opaque container blocks visual verification of hidden internal items."
            })
        elif observability == "PARTIALLY_OBSERVABLE":
            items.append({
                "status": "WARNING",
                "source": "Observability",
                "message": "Container contents are only partially observable.",
                "technical_value": "PARTIALLY_OBSERVABLE",
                "explanation": "Semi-opaque material partially obscures internal contents."
            })
        else:
            items.append({
                "status": "PASS",
                "source": "Observability",
                "message": "Container material is clear and contents are observable.",
                "technical_value": "OBSERVABLE",
                "explanation": "Transparent container allows full visual inspection."
            })
            
        # 5. Conflict Check
        if "BARCODE_VISUAL_CONFLICT" in conflict_codes:
            items.append({
                "status": "FAIL",
                "source": "Barcode Cross-Check",
                "message": "Scanned barcode category conflicts with visual evidence.",
                "technical_value": "CONFLICT_DETECTED",
                "explanation": "CPCB barcode string category does not match visual classification."
            })
            
        # 6. Weight Anomaly Check
        if z_score >= 2.5:
            items.append({
                "status": "WARNING",
                "source": "Weight Anomaly",
                "message": f"Weight deviates significantly from department baseline (Z = +{z_score:.1f}).",
                "technical_value": f"Z={z_score:.1f}",
                "explanation": "Container mass differs from normal historical distribution for this ward."
            })
            
        return items
