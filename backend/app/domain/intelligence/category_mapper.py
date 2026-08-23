from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class WasteCategoryMapping:
    object_class: str
    waste_type: str        # SHARPS, CONTAMINATED_PLASTIC, SOILED_WASTE, PHARMACEUTICAL, CONTAMINATED_GLASS, UNKNOWN
    bag_category: str      # WHITE, RED, YELLOW, BLUE, UNKNOWN
    hazard_level: str      # CRITICAL, HIGH, MEDIUM, LOW, UNKNOWN
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "object_class": self.object_class,
            "waste_type": self.waste_type,
            "bag_category": self.bag_category,
            "hazard_level": self.hazard_level,
            "description": self.description
        }

class WasteCategoryMapper:
    """
    Centralized Biomedical Waste Category Mapping Engine.
    Maps physical detected object classes to waste types and disposal bag categories.
    NEVER uses YELLOW as a fallback for unknown objects (unknown objects map to UNKNOWN).
    """

    MAPPINGS: Dict[str, Dict[str, str]] = {
        "syringe": {
            "waste_type": "SHARPS",
            "bag_category": "WHITE",
            "hazard_level": "CRITICAL",
            "description": "Contaminated hypodermic syringe requiring puncture-proof sharp container"
        },
        "needle": {
            "waste_type": "SHARPS",
            "bag_category": "WHITE",
            "hazard_level": "CRITICAL",
            "description": "Contaminated needle point requiring puncture-proof sharp container"
        },
        "scalpel": {
            "waste_type": "SHARPS",
            "bag_category": "WHITE",
            "hazard_level": "CRITICAL",
            "description": "Surgical blade / scalpel requiring puncture-proof sharp container"
        },
        "blade": {
            "waste_type": "SHARPS",
            "bag_category": "WHITE",
            "hazard_level": "CRITICAL",
            "description": "Medical blade / razor requiring puncture-proof sharp container"
        },
        "lancet": {
            "waste_type": "SHARPS",
            "bag_category": "WHITE",
            "hazard_level": "CRITICAL",
            "description": "Blood sampling lancet requiring puncture-proof sharp container"
        },
        "iv_tube": {
            "waste_type": "CONTAMINATED_PLASTIC",
            "bag_category": "RED",
            "hazard_level": "HIGH",
            "description": "Contaminated plastic tubing suitable for autoclave & recycling"
        },
        "catheter": {
            "waste_type": "CONTAMINATED_PLASTIC",
            "bag_category": "RED",
            "hazard_level": "HIGH",
            "description": "Flexible plastic catheter suitable for autoclave & recycling"
        },
        "urine_bag": {
            "waste_type": "CONTAMINATED_PLASTIC",
            "bag_category": "RED",
            "hazard_level": "HIGH",
            "description": "Contaminated plastic drainage bag suitable for autoclave & recycling"
        },
        "blood_bag": {
            "waste_type": "CONTAMINATED_PLASTIC",
            "bag_category": "RED",
            "hazard_level": "HIGH",
            "description": "Empty plastic blood bag suitable for autoclave & recycling"
        },
        "gloves": {
            "waste_type": "CONTAMINATED_PLASTIC",
            "bag_category": "RED",
            "hazard_level": "MEDIUM",
            "description": "Disposable latex / nitrile examination gloves"
        },
        "mask": {
            "waste_type": "CONTAMINATED_PPE",
            "bag_category": "RED",
            "hazard_level": "MEDIUM",
            "description": "Disposable surgical / N95 medical mask"
        },
        "gauze": {
            "waste_type": "SOILED_WASTE",
            "bag_category": "YELLOW",
            "hazard_level": "HIGH",
            "description": "Soiled cotton / dressing for high-temperature incineration"
        },
        "blood_soaked_gauze": {
            "waste_type": "SOILED_WASTE",
            "bag_category": "YELLOW",
            "hazard_level": "HIGH",
            "description": "Blood-soaked cotton / surgical dressing for incineration"
        },
        "cotton": {
            "waste_type": "SOILED_WASTE",
            "bag_category": "YELLOW",
            "hazard_level": "HIGH",
            "description": "Soiled medical cotton swab for incineration"
        },
        "human_tissue": {
            "waste_type": "ANATOMICAL_WASTE",
            "bag_category": "YELLOW",
            "hazard_level": "CRITICAL",
            "description": "Anatomical / biological tissue specimen for incineration"
        },
        "medicine_vial": {
            "waste_type": "PHARMACEUTICAL",
            "bag_category": "BLUE",
            "hazard_level": "MEDIUM",
            "description": "Glass medicine vial / container for glass recycling"
        },
        "glass_ampoule": {
            "waste_type": "CONTAMINATED_GLASS",
            "bag_category": "BLUE",
            "hazard_level": "HIGH",
            "description": "Broken or intact glass ampoule requiring blue bin recycling"
        },
        "laboratory_glass": {
            "waste_type": "CONTAMINATED_GLASS",
            "bag_category": "BLUE",
            "hazard_level": "HIGH",
            "description": "Laboratory glass tube / slide for glass recycling"
        },
        "unknown": {
            "waste_type": "UNKNOWN",
            "bag_category": "UNKNOWN",
            "hazard_level": "UNKNOWN",
            "description": "Unidentified or unclassified medical item requiring human inspection"
        }
    }

    @classmethod
    def map_object_to_category(cls, object_class: str) -> WasteCategoryMapping:
        normalized = (object_class or "unknown").strip().lower().replace("-", "_").replace(" ", "_")
        
        matched_key = "unknown"
        if "syringe" in normalized:
            matched_key = "syringe"
        elif "needle" in normalized:
            matched_key = "needle"
        elif "scalpel" in normalized:
            matched_key = "scalpel"
        elif "blade" in normalized:
            matched_key = "blade"
        elif "lancet" in normalized:
            matched_key = "lancet"
        elif "ampoule" in normalized or "glass_ampoule" in normalized or "laboratory_glass" in normalized:
            matched_key = "glass_ampoule"
        elif "vial" in normalized or "medicine_vial" in normalized:
            matched_key = "medicine_vial"
        elif "iv" in normalized or "tube" in normalized or "catheter" in normalized:
            matched_key = "iv_tube"
        elif "glove" in normalized:
            matched_key = "gloves"
        elif "mask" in normalized:
            matched_key = "mask"
        elif "gauze" in normalized or "dressing" in normalized or "cotton" in normalized:
            matched_key = "gauze"
        elif normalized in cls.MAPPINGS:
            matched_key = normalized
            
        data = cls.MAPPINGS.get(matched_key, cls.MAPPINGS["unknown"])
        
        return WasteCategoryMapping(
            object_class=object_class.upper() if object_class else "UNKNOWN",
            waste_type=data["waste_type"],
            bag_category=data["bag_category"],
            hazard_level=data["hazard_level"],
            description=data["description"]
        )
