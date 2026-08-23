from typing import List, Dict, Any

class ReasoningPanelEngine:
    """
    Generates structured human-readable reasons for the 'Why Not?' UI panel.
    Statuses: PASS, WARNING, FAIL.
    """
    @staticmethod
    def generate_reasons(
        quality_score: float,
        confidence: float,
        observability: str,
        conflict_codes: List[str],
        uncertainty_score: float,
        z_score: float
    ) -> List[Dict[str, Any]]:
        items = []
        
        # Image Quality
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
            
        # AI Confidence
        items.append({
            "status": "PASS" if confidence >= 0.80 else "WARNING",
            "source": "AI Confidence",
            "message": f"Model prediction confidence is {confidence * 100:.1f}%.",
            "technical_value": f"{confidence:.2f}",
            "explanation": "High raw model confidence does not guarantee operational safety."
        })
        
        # Observability
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
            
        # Conflict Check
        if "BARCODE_VISUAL_CONFLICT" in conflict_codes:
            items.append({
                "status": "FAIL",
                "source": "Barcode Cross-Check",
                "message": "Scanned barcode category conflicts with visual evidence.",
                "technical_value": "CONFLICT_DETECTED",
                "explanation": "CPCB barcode string category does not match visual classification."
            })
            
        # Weight Anomaly Check
        if z_score >= 2.5:
            items.append({
                "status": "WARNING",
                "source": "Weight Anomaly",
                "message": f"Weight deviates significantly from department baseline (Z = +{z_score:.1f}).",
                "technical_value": f"Z={z_score:.1f}",
                "explanation": "Container mass differs from normal historical distribution for this ward."
            })
            
        return items
