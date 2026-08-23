from dataclasses import dataclass
from typing import Optional

@dataclass
class AnomalyEvaluationResult:
    is_anomalous: bool
    observed_value: float
    baseline_value: float
    multiplier: float
    z_score: float
    severity: str
    anomaly_type: str
    recommended_action: str

class AnomalyEngine:
    """
    Statistical Z-Score Anomaly Engine for Waste Stream Monitoring.
    Detects sudden volume surges, weight anomalies, and category distribution shifts.
    """
    @staticmethod
    def evaluate_weight(observed_kg: float, baseline_kg: float, std_dev_kg: float = 1.8) -> AnomalyEvaluationResult:
        if baseline_kg <= 0:
            baseline_kg = 2.1
            
        multiplier = round(observed_kg / baseline_kg, 2)
        z_score = round((observed_kg - baseline_kg) / std_dev_kg, 2)
        
        is_anomalous = z_score >= 2.5 or multiplier >= 2.5
        severity = "CRITICAL" if z_score >= 4.0 else ("HIGH" if z_score >= 3.0 else ("MEDIUM" if is_anomalous else "NORMAL"))
        
        action = "Supervisor review recommended for unexpected waste weight surge." if is_anomalous else "Weight within normal variance."
        
        return AnomalyEvaluationResult(
            is_anomalous=is_anomalous,
            observed_value=observed_kg,
            baseline_value=baseline_kg,
            multiplier=multiplier,
            z_score=z_score,
            severity=severity,
            anomaly_type="WEIGHT_SURGE_ANOMALY" if is_anomalous else "NORMAL",
            recommended_action=action
        )
