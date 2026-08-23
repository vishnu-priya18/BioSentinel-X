import pytest
from app.domain.intelligence.category_mapper import WasteCategoryMapper

def test_syringe_maps_to_white():
    res = WasteCategoryMapper.map_object_to_category("syringe")
    assert res.object_class == "SYRINGE"
    assert res.waste_type == "SHARPS"
    assert res.bag_category == "WHITE"
    assert res.bag_category != "YELLOW"

def test_needle_maps_to_white():
    res = WasteCategoryMapper.map_object_to_category("needle")
    assert res.object_class == "NEEDLE"
    assert res.waste_type == "SHARPS"
    assert res.bag_category == "WHITE"
    assert res.bag_category != "YELLOW"

def test_scalpel_maps_to_white():
    res = WasteCategoryMapper.map_object_to_category("scalpel")
    assert res.object_class == "SCALPEL"
    assert res.waste_type == "SHARPS"
    assert res.bag_category == "WHITE"
    assert res.bag_category != "YELLOW"

def test_blade_maps_to_white():
    res = WasteCategoryMapper.map_object_to_category("blade")
    assert res.object_class == "BLADE"
    assert res.waste_type == "SHARPS"
    assert res.bag_category == "WHITE"
    assert res.bag_category != "YELLOW"

def test_lancet_maps_to_white():
    res = WasteCategoryMapper.map_object_to_category("lancet")
    assert res.object_class == "LANCET"
    assert res.waste_type == "SHARPS"
    assert res.bag_category == "WHITE"
    assert res.bag_category != "YELLOW"

def test_iv_tube_maps_to_red():
    res = WasteCategoryMapper.map_object_to_category("iv_tube")
    assert res.waste_type == "CONTAMINATED_PLASTIC"
    assert res.bag_category == "RED"
    assert res.bag_category != "YELLOW"

def test_catheter_maps_to_red():
    res = WasteCategoryMapper.map_object_to_category("catheter")
    assert res.waste_type == "CONTAMINATED_PLASTIC"
    assert res.bag_category == "RED"

def test_gloves_maps_to_red():
    res = WasteCategoryMapper.map_object_to_category("gloves")
    assert res.waste_type == "CONTAMINATED_PLASTIC"
    assert res.bag_category == "RED"

def test_gauze_maps_to_yellow():
    res = WasteCategoryMapper.map_object_to_category("gauze")
    assert res.waste_type == "SOILED_WASTE"
    assert res.bag_category == "YELLOW"

def test_blood_soaked_gauze_maps_to_yellow():
    res = WasteCategoryMapper.map_object_to_category("blood_soaked_gauze")
    assert res.waste_type == "SOILED_WASTE"
    assert res.bag_category == "YELLOW"

def test_glass_ampoule_maps_to_blue():
    res = WasteCategoryMapper.map_object_to_category("glass_ampoule")
    assert res.waste_type == "CONTAMINATED_GLASS"
    assert res.bag_category == "BLUE"
    assert res.bag_category != "YELLOW"

def test_unknown_maps_to_unknown():
    res = WasteCategoryMapper.map_object_to_category("unknown_random_item")
    assert res.waste_type == "UNKNOWN"
    assert res.bag_category == "UNKNOWN"
    assert res.bag_category != "YELLOW"
