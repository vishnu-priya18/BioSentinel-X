from typing import List, Dict, Any

class RegulatoryRules:
    """
    Configurable Regulatory Compliance Workflow Engine.
    Enforces CPCB 2016 rules without hardcoding unsupported claims.
    """
    @staticmethod
    def get_default_rules() -> List[Dict[str, Any]]:
        return [
            {
                "rule_id": "RULE-CPCB-001",
                "jurisdiction": "INDIA_CPCB_2016",
                "category": "Yellow",
                "required_treatment": "INCINERATION_OR_DEEP_BURIAL",
                "barcode_mandatory": True,
                "max_storage_hours": 48,
                "description": "Anatomical waste, soiled cotton, chemical waste."
            },
            {
                "rule_id": "RULE-CPCB-002",
                "jurisdiction": "INDIA_CPCB_2016",
                "category": "Red",
                "required_treatment": "AUTOCLAVE_SHREDDING_RECYCLING",
                "barcode_mandatory": True,
                "max_storage_hours": 48,
                "description": "Contaminated recyclable plastics (tubing, IV bottles, catheters)."
            },
            {
                "rule_id": "RULE-CPCB-003",
                "jurisdiction": "INDIA_CPCB_2016",
                "category": "White",
                "required_treatment": "AUTOCLAVE_SHREDDING_IRON_FOUNDRY",
                "barcode_mandatory": True,
                "max_storage_hours": 48,
                "description": "Waste sharps including needles, scalpels, blades in puncture-proof containers."
            },
            {
                "rule_id": "RULE-CPCB-004",
                "jurisdiction": "INDIA_CPCB_2016",
                "category": "Blue",
                "required_treatment": "DISINFECTION_SODIUM_HYPOCHLORITE_RECYCLING",
                "barcode_mandatory": True,
                "max_storage_hours": 48,
                "description": "Glassware and metallic body implants."
            }
        ]
