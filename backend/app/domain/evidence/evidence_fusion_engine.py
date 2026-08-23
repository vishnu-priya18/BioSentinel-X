from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class EvidenceFusionResult:
    visual_support: float
    barcode_support: float
    weight_support: float
    historical_support: float
    hazard_support: float
    observability: str
    missing_evidence: List[str]
    conflict_score: float
    conflict_codes: List[str]

class EvidenceFusionEngine:
    """
    Fuses visual, barcode, weight, department history, hazard evidence, and user observation evidence.
    Calculates conflict_score and conflict_codes without allowing category confidence to override critical hazards.
    """
    @staticmethod
    def fuse(
        declared_category: str,
        predicted_category: str,
        barcode_scanned: str,
        weight_kg: float,
        baseline_weight_kg: float,
        observability: str,
        quality_score: float,
        hazard_result: Optional[Any] = None
    ) -> EvidenceFusionResult:
        missing_evidence = []
        conflict_codes = []
        
        # Check missing evidence
        if quality_score < 0.40:
            missing_evidence.append("LOW_IMAGE_QUALITY")
        if not barcode_scanned:
            missing_evidence.append("MISSING_BARCODE")
            
        # Support calculations
        visual_support = quality_score if observability != "NOT_OBSERVABLE" else 0.10
        
        # Hazard support calculation
        hazard_support = 1.0
        if hazard_result and hazard_result.detected:
            hazard_support = hazard_result.score
            if hazard_result.critical_hazard:
                conflict_codes.append("CRITICAL_SHARP_HAZARD")
        
        # Barcode support & conflict check
        barcode_support = 1.0
        if barcode_scanned and declared_category:
            barcode_cat = "YELLOW" if "YEL" in barcode_scanned.upper() else ("RED" if "RED" in barcode_scanned.upper() else "UNKNOWN")
            if barcode_cat != "UNKNOWN" and barcode_cat.upper() != predicted_category.upper():
                barcode_support = 0.12
                conflict_codes.append("BARCODE_VISUAL_CONFLICT")
                
        # Weight support & conflict check
        weight_support = 1.0
        if baseline_weight_kg > 0:
            ratio = weight_kg / baseline_weight_kg
            if ratio > 2.5 or ratio < 0.2:
                weight_support = 0.31
                conflict_codes.append("ABNORMAL_WEIGHT")
                
        historical_support = 0.85
        
        # Calculate overall conflict score [0.0, 1.0]
        conflict_score = 0.0
        if "CRITICAL_SHARP_HAZARD" in conflict_codes:
            conflict_score += 0.50
        if "BARCODE_VISUAL_CONFLICT" in conflict_codes:
            conflict_score += 0.45
        if "ABNORMAL_WEIGHT" in conflict_codes:
            conflict_score += 0.35
            
        conflict_score = min(1.0, conflict_score)
        
        return EvidenceFusionResult(
            visual_support=visual_support,
            barcode_support=barcode_support,
            weight_support=weight_support,
            historical_support=historical_support,
            hazard_support=hazard_support,
            observability=observability,
            missing_evidence=missing_evidence,
            conflict_score=conflict_score,
            conflict_codes=conflict_codes
        )
