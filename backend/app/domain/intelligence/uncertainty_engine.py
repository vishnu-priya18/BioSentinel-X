import math
from typing import Dict
from dataclasses import dataclass

@dataclass
class UncertaintyResult:
    entropy: float
    uncertainty_score: float
    level_enum: str # LOW_UNCERTAINTY, MEDIUM_UNCERTAINTY, HIGH_UNCERTAINTY
    calibration_status: str

class UncertaintyEngine:
    """
    Calculates Softmax Uncertainty Entropy H(x) and calibrated uncertainty score.
    Returns UncertaintyResult. Never directly decides operational action.
    """
    @staticmethod
    def calculate(probabilities: Dict[str, float], quality_score: float, observability: str) -> UncertaintyResult:
        # Calculate Shannon Softmax Entropy H(x)
        entropy = 0.0
        for p in probabilities.values():
            if p > 0:
                entropy -= p * math.log2(p)
                
        # Normalize entropy over 4 categories (max entropy = log2(4) = 2.0)
        normalized_entropy = min(1.0, entropy / 2.0)
        
        # Calibrated uncertainty fusing entropy, image quality, and opacity
        quality_penalty = (1.0 - quality_score) * 0.40
        opacity_penalty = 0.50 if observability == "NOT_OBSERVABLE" else (0.25 if observability == "PARTIALLY_OBSERVABLE" else 0.0)
        
        uncertainty_score = min(1.0, normalized_entropy * 0.5 + quality_penalty + opacity_penalty)
        
        if uncertainty_score >= 0.60:
            level = "HIGH_UNCERTAINTY"
        elif uncertainty_score >= 0.35:
            level = "MEDIUM_UNCERTAINTY"
        else:
            level = "LOW_UNCERTAINTY"
            
        return UncertaintyResult(
            entropy=round(entropy, 4),
            uncertainty_score=round(uncertainty_score, 4),
            level_enum=level,
            calibration_status="CALIBRATED_PROTOTYPE_DATASET"
        )
