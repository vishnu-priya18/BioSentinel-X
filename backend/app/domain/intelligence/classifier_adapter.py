from typing import Protocol, Dict, Any, Optional
from dataclasses import dataclass
from app.domain.intelligence.category_mapper import WasteCategoryMapper

@dataclass
class ClassificationResult:
    object_class: str
    waste_type: str
    bag_category: str
    predicted_category: str
    confidence: float
    probabilities: Dict[str, float]
    model_version: str
    inference_ms: float

class WasteClassifier(Protocol):
    def predict(self, image_base64: Optional[str] = None, metadata: Optional[dict] = None) -> ClassificationResult:
        ...

class DemoWasteClassifier:
    """
    Deterministic Prototype Simulator for SIH Demonstration.
    Clearly labeled as DEMO SIMULATION MODEL.
    Separates Physical Object Detection -> Category Mapping -> Hazard Gate Authorization.
    NEVER defaults to YELLOW for uncertain or sharp objects.
    """
    def predict(self, image_base64: Optional[str] = None, metadata: Optional[dict] = None) -> ClassificationResult:
        metadata = metadata or {}
        model_ver = "DEMO_SIMULATION_MODEL_V1.0"
        
        code = metadata.get("scenario_code", "")
        item_desc = (metadata.get("item_description") or "").lower()
        declared_cat = metadata.get("declared_category", "")
        
        object_name = "unknown"
        confidence = 0.85
        
        if code == "DEMO-001":
            object_name = "iv_tube"
            confidence = 0.94
        elif code == "DEMO-002":
            object_name = "gauze"
            confidence = 0.62
        elif code == "DEMO-003":
            object_name = "unknown"
            confidence = 0.50
        elif code == "DEMO-004":
            object_name = "iv_tube"
            confidence = 0.88
        elif code == "DEMO-005" or "syringe" in item_desc or "injection" in item_desc or "needle" in item_desc or "scalpel" in item_desc or "blade" in item_desc:
            if "needle" in item_desc:
                object_name = "needle"
            elif "scalpel" in item_desc:
                object_name = "scalpel"
            elif "blade" in item_desc:
                object_name = "blade"
            else:
                object_name = "syringe"
            confidence = 0.97
        elif "glass" in item_desc or "vial" in item_desc or "ampoule" in item_desc:
            object_name = "medicine_vial"
            confidence = 0.92
        elif "gauze" in item_desc or "cotton" in item_desc:
            object_name = "gauze"
            confidence = 0.89
        elif "tube" in item_desc or "catheter" in item_desc:
            object_name = "iv_tube"
            confidence = 0.91
        elif declared_cat and declared_cat.upper() != "UNKNOWN":
            if declared_cat.upper() == "RED":
                object_name = "iv_tube"
            elif declared_cat.upper() == "WHITE":
                object_name = "syringe"
            elif declared_cat.upper() == "BLUE":
                object_name = "medicine_vial"
            elif declared_cat.upper() == "YELLOW":
                object_name = "gauze"

        mapping = WasteCategoryMapper.map_object_to_category(object_name)
        
        probs = {"Yellow": 0.05, "Red": 0.05, "White": 0.05, "Blue": 0.05, "Unknown": 0.05}
        cat_key = mapping.bag_category.capitalize()
        if cat_key in probs:
            probs[cat_key] = confidence
        else:
            probs["Unknown"] = confidence

        return ClassificationResult(
            object_class=mapping.object_class,
            waste_type=mapping.waste_type,
            bag_category=mapping.bag_category,
            predicted_category=mapping.bag_category,
            confidence=confidence,
            probabilities=probs,
            model_version=model_ver,
            inference_ms=30.0
        )

class ONNXWasteClassifierAdapter:
    """
    Placeholder adapter for future ONNX production ML model integration.
    """
    def predict(self, image_base64: Optional[str] = None, metadata: Optional[dict] = None) -> ClassificationResult:
        return DemoWasteClassifier().predict(image_base64, metadata)
