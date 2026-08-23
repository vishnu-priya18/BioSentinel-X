import pytest
from app.domain.intelligence.object_detector import WasteObjectDetector

def test_object_detector_syringe():
    res = WasteObjectDetector.detect(metadata={"item_description": "Hypodermic Syringe"})
    assert res.detector_status == "SUCCESS"
    assert len(res.objects) >= 1
    primary = res.primary_object
    assert primary is not None
    assert primary.class_name == "SYRINGE"
    assert primary.confidence >= 0.90
    assert primary.bounding_box.x1 < primary.bounding_box.x2
    assert primary.hazard_type == "SHARP"
    assert primary.hazard_severity == "CRITICAL"

def test_object_detector_needle():
    res = WasteObjectDetector.detect(metadata={"item_description": "Surgical Needle"})
    assert res.detector_status == "SUCCESS"
    primary = res.primary_object
    assert primary is not None
    assert primary.class_name == "SYRINGE" or primary.class_name == "NEEDLE"
    assert primary.hazard_severity == "CRITICAL"

def test_object_detector_scalpel():
    res = WasteObjectDetector.detect(metadata={"item_description": "Scalpel Blade"})
    assert res.detector_status == "SUCCESS"
    primary = res.primary_object
    assert primary is not None
    assert primary.class_name == "SCALPEL"
    assert primary.hazard_severity == "CRITICAL"

def test_object_detector_gauze():
    res = WasteObjectDetector.detect(metadata={"item_description": "Soiled Gauze"})
    assert res.detector_status == "SUCCESS"
    primary = res.primary_object
    assert primary is not None
    assert primary.class_name == "BLOOD_STAINED_GAUZE"
    assert primary.hazard_type == "INFECTIOUS"

def test_object_detector_glass_vial():
    res = WasteObjectDetector.detect(metadata={"item_description": "Medicine Glass Ampoule"})
    assert res.detector_status == "SUCCESS"
    primary = res.primary_object
    assert primary is not None
    assert primary.class_name == "GLASS_VIAL"
    assert primary.hazard_type == "GLASS"

def test_object_detector_unknown():
    res = WasteObjectDetector.detect(metadata={"item_description": "Unrecognized random plastic"})
    assert res.detector_status == "NO_OBJECT_DETECTED"
    assert res.primary_object is None
