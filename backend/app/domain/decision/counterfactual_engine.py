from typing import List, Dict, Any

class CounterfactualEngine:
    """
    Evaluates 'What would have made this safe?'
    Returns explicit required evidence conditions for safe automation.
    """
    @staticmethod
    def evaluate_required_conditions(
        observability: str,
        conflict_codes: List[str],
        uncertainty_score: float,
        quality_score: float
    ) -> List[str]:
        required = []
        
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
