from typing import Protocol, Dict, Any
from dataclasses import dataclass

@dataclass
class ClassificationResult:
    predicted_category: str
    confidence: float
    probabilities: Dict[str, float]
    model_version: str
    inference_ms: float

class WasteClassifier(Protocol):
    def predict(self, image_base64: str, metadata: dict) -> ClassificationResult:
        ...

class DemoWasteClassifier:
    """
    Deterministic Prototype Simulator for SIH Demonstration.
    Clearly labeled as DEMO SIMULATION MODEL.
    """
    def predict(self, image_base64: str = None, metadata: dict = None) -> ClassificationResult:
        model_ver = "DEMO_SIMULATION_MODEL_V1.0"
        
        # Check scenario overrides for deterministic DEMO-001 to DEMO-008 testing
        if metadata and "scenario_code" in metadata:
            code = metadata["scenario_code"]
            if code == "DEMO-001":
                return ClassificationResult(
                    predicted_category="Red",
                    confidence=0.94,
                    probabilities={"Yellow": 0.02, "Red": 0.94, "White": 0.02, "Blue": 0.02},
                    model_version=model_ver,
                    inference_ms=32.0
                )
            elif code == "DEMO-003":
                return ClassificationResult(
                    predicted_category="Red",
                    confidence=0.91,
                    probabilities={"Yellow": 0.05, "Red": 0.91, "White": 0.02, "Blue": 0.02},
                    model_version=model_ver,
                    inference_ms=35.0
                )
            elif code == "DEMO-004":
                return ClassificationResult(
                    predicted_category="Red",
                    confidence=0.88,
                    probabilities={"Yellow": 0.08, "Red": 0.88, "White": 0.02, "Blue": 0.02},
                    model_version=model_ver,
                    inference_ms=30.0
                )
                
        # Default category determination based on declared category
        declared = (metadata.get("declared_category") or "Red").capitalize()
        if declared not in ["Yellow", "Red", "White", "Blue"]:
            declared = "Red"
            
        probs = {"Yellow": 0.05, "Red": 0.05, "White": 0.05, "Blue": 0.05}
        probs[declared] = 0.85
        
        return ClassificationResult(
            predicted_category=declared,
            confidence=0.85,
            probabilities=probs,
            model_version=model_ver,
            inference_ms=34.0
        )

class ONNXWasteClassifierAdapter:
    """
    Placeholder adapter for future ONNX production ML model integration.
    """
    def predict(self, image_base64: str, metadata: dict) -> ClassificationResult:
        # Fallback to Demo Classifier for prototype build
        return DemoWasteClassifier().predict(image_base64, metadata)
