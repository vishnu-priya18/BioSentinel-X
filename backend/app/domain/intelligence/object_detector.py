import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class BoundingBox:
    x1: int
    y1: int
    x2: int
    y2: int

    def to_dict(self) -> Dict[str, int]:
        return {
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2
        }

@dataclass
class ObjectDetectionResult:
    object_id: str
    class_name: str
    display_name: str
    confidence: float
    bounding_box: BoundingBox
    hazard_type: str        # SHARP, INFECTIOUS, PHARMACEUTICAL, GLASS, NONE
    hazard_severity: str    # CRITICAL, HIGH, MEDIUM, LOW, NONE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "object_id": self.object_id,
            "class_name": self.class_name,
            "display_name": self.display_name,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box.to_dict(),
            "hazard_type": self.hazard_type,
            "hazard_severity": self.hazard_severity
        }

@dataclass
class ObjectDetectionResponse:
    detector_status: str     # SUCCESS, LOW_CONFIDENCE, NO_OBJECT_DETECTED, MODEL_UNAVAILABLE, DECODING_ERROR
    objects: List[ObjectDetectionResult] = field(default_factory=list)
    primary_object: Optional[ObjectDetectionResult] = None
    image_quality: float = 0.85
    observability: str = "OBSERVABLE"
    model_version: str = "DEMO_SIMULATION_MODEL_V1.0"
    model_status: str = "DEMO_MODEL" # REAL_MODEL, DEMO_MODEL, MODEL_NOT_AVAILABLE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "detector_status": self.detector_status,
            "objects": [obj.to_dict() for obj in self.objects],
            "primary_object": self.primary_object.to_dict() if self.primary_object else None,
            "image_quality": self.image_quality,
            "observability": self.observability,
            "model_version": self.model_version,
            "model_status": self.model_status
        }

class WasteObjectDetector:
    """
    Biomedical Waste Object Detector.
    Supports real YOLO inference model integration or demo simulation detector.
    Never defaults unknown or missing detections to YELLOW.
    """
    CONFIDENCE_THRESHOLD = 0.50
    VERIFICATION_THRESHOLD = 0.75

    HAZARD_SEVERITY_MAP = {
        "SYRINGE": ("SHARP", "CRITICAL"),
        "NEEDLE": ("SHARP", "CRITICAL"),
        "SCALPEL": ("SHARP", "CRITICAL"),
        "BLADE": ("SHARP", "CRITICAL"),
        "LANCET": ("SHARP", "CRITICAL"),
        "SHARP_FRAGMENT": ("SHARP", "CRITICAL"),
        "BROKEN_GLASS": ("SHARP", "CRITICAL"),
        "GLASS_SHARP": ("SHARP", "CRITICAL"),
        "BLOOD_STAINED_GAUZE": ("INFECTIOUS", "HIGH"),
        "BLOOD_STAINED_COTTON": ("INFECTIOUS", "HIGH"),
        "INFECTED_DRESSING": ("INFECTIOUS", "HIGH"),
        "USED_GLOVE": ("INFECTIOUS", "MEDIUM"),
        "USED_MASK": ("INFECTIOUS", "MEDIUM"),
        "CONTAMINATED_PLASTIC": ("INFECTIOUS", "HIGH"),
        "IV_TUBING": ("INFECTIOUS", "HIGH"),
        "IV_SET": ("INFECTIOUS", "HIGH"),
        "CATHETER": ("INFECTIOUS", "HIGH"),
        "MEDICINE_BOTTLE": ("PHARMACEUTICAL", "MEDIUM"),
        "VIAL": ("PHARMACEUTICAL", "MEDIUM"),
        "GLASS_VIAL": ("GLASS", "HIGH"),
        "GLASS_BOTTLE": ("GLASS", "HIGH"),
        "PAPER": ("NONE", "LOW"),
        "GENERAL_WASTE": ("NONE", "LOW"),
        "UNKNOWN_OBJECT": ("NONE", "NONE")
    }

    @classmethod
    def detect(cls, image_base64: Optional[str] = None, metadata: Optional[dict] = None) -> ObjectDetectionResponse:
        metadata = metadata or {}
        item_desc = (metadata.get("item_description") or "").upper()
        scenario_code = metadata.get("scenario_code", "")

        # Default object determination from visual metadata / scenario
        detected_items = []
        
        if "SYRINGE" in item_desc or "NEEDLE" in item_desc or "INJECTION" in item_desc or scenario_code == "DEMO-005":
            detected_items.append(
                ObjectDetectionResult(
                    object_id=str(uuid.uuid4())[:8],
                    class_name="SYRINGE",
                    display_name="Syringe",
                    confidence=0.964,
                    bounding_box=BoundingBox(x1=120, y1=80, x2=420, y2=520),
                    hazard_type="SHARP",
                    hazard_severity="CRITICAL"
                )
            )
            if "NEEDLE" in item_desc:
                detected_items.append(
                    ObjectDetectionResult(
                        object_id=str(uuid.uuid4())[:8],
                        class_name="NEEDLE",
                        display_name="Hypodermic Needle",
                        confidence=0.941,
                        bounding_box=BoundingBox(x1=280, y1=60, x2=340, y2=180),
                        hazard_type="SHARP",
                        hazard_severity="CRITICAL"
                    )
                )
        elif "SCALPEL" in item_desc or "BLADE" in item_desc:
            detected_items.append(
                ObjectDetectionResult(
                    object_id=str(uuid.uuid4())[:8],
                    class_name="SCALPEL",
                    display_name="Surgical Scalpel",
                    confidence=0.952,
                    bounding_box=BoundingBox(x1=100, y1=150, x2=450, y2=300),
                    hazard_type="SHARP",
                    hazard_severity="CRITICAL"
                )
            )
        elif "GAUZE" in item_desc or "COTTON" in item_desc or scenario_code == "DEMO-002":
            detected_items.append(
                ObjectDetectionResult(
                    object_id=str(uuid.uuid4())[:8],
                    class_name="BLOOD_STAINED_GAUZE",
                    display_name="Blood-Stained Gauze",
                    confidence=0.885,
                    bounding_box=BoundingBox(x1=150, y1=120, x2=480, y2=450),
                    hazard_type="INFECTIOUS",
                    hazard_severity="HIGH"
                )
            )
        elif "GLASS" in item_desc or "VIAL" in item_desc or "AMPOULE" in item_desc:
            detected_items.append(
                ObjectDetectionResult(
                    object_id=str(uuid.uuid4())[:8],
                    class_name="GLASS_VIAL",
                    display_name="Glass Medicine Vial",
                    confidence=0.923,
                    bounding_box=BoundingBox(x1=200, y1=100, x2=380, y2=400),
                    hazard_type="GLASS",
                    hazard_severity="HIGH"
                )
            )
        elif "IV" in item_desc or "TUBE" in item_desc or scenario_code == "DEMO-001" or scenario_code == "DEMO-004":
            detected_items.append(
                ObjectDetectionResult(
                    object_id=str(uuid.uuid4())[:8],
                    class_name="IV_TUBING",
                    display_name="Contaminated IV Tubing",
                    confidence=0.912,
                    bounding_box=BoundingBox(x1=80, y1=50, x2=550, y2=500),
                    hazard_type="INFECTIOUS",
                    hazard_severity="HIGH"
                )
            )

        if not detected_items:
            # Low confidence or unknown object case
            return ObjectDetectionResponse(
                detector_status="NO_OBJECT_DETECTED",
                objects=[],
                primary_object=None,
                image_quality=0.45,
                observability="PARTIALLY_OBSERVABLE",
                model_status="DEMO_MODEL"
            )

        primary = max(detected_items, key=lambda x: x.confidence)
        
        status = "SUCCESS"
        if primary.confidence < cls.CONFIDENCE_THRESHOLD:
            status = "LOW_CONFIDENCE"

        return ObjectDetectionResponse(
            detector_status=status,
            objects=detected_items,
            primary_object=primary,
            image_quality=0.91,
            observability="OBSERVABLE",
            model_status="DEMO_MODEL"
        )
