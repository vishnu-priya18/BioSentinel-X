from typing import List, Dict, Any, Optional

class CounterfactualEngine:
    """
    Evaluates 'What would make this safe?'
    Returns explicit required evidence conditions for safe automation.
    AI confidence alone cannot authorize automated handling of a sharp hazard.
    """
    @staticmethod
    def evaluate_required_conditions(
        observability: str,
        conflict_codes: List[str],
        uncertainty_score: float,
        quality_score: float,
        hazard_result: Optional[Any] = None
    ) -> List[str]:
        required = []
        
        # Hazard clearance requirements
        if hazard_result and hazard_result.detected:
            if hazard_result.critical_hazard:
                required.append("HAZARD_CLEARANCE_AND_INDEPENDENT_VERIFICATION")
                required.append("SAFE_SHARPS_HANDLING_WORKFLOW_CONFIRMATION")
                required.append("AUTHORIZED_HUMAN_VERIFIER_SIGN_OFF")
            else:
                required.append("HAZARD_RISK_VERIFICATION")
        
        if observability == "NOT_OBSERVABLE":
            required.append("OBSERVABLE_CONTENT_OR_TRANSPARENT_CONTAINER")
            
        if "BARCODE_VISUAL_CONFLICT" in conflict_codes:
            required.append("VALID_CATEGORY_BARCODE_MATCH")
            
        if "ABNORMAL_WEIGHT" in conflict_codes:
            required.append("NORMAL_DEPARTMENT_WEIGHT_BASELINE")
            
        if quality_score < 0.40:
            required.append("HIGH_QUALITY_IMAGE_CAPTURE")
            
        if uncertainty_score >= 0.35:
            required.append("CONFIRMED_LOW_UNCERTAINTY_METRICS")
            
        if not required:
            required.append("ALL_SAFETY_BOUNDS_SATISFIED")
            
        return required
