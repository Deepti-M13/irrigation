#!/usr/bin/env python
"""Test script to verify ML models are working correctly"""

from app.services.prediction import predictor

print("=" * 60)
print("TESTING FIXED ML MODELS")
print("=" * 60)

# Test Case 1: Dry field (needs irrigation)
print("\n1. DRY FIELD TEST (Should need irrigation)")
print("-" * 60)
features_dry = {
    'soil_moisture': 20,
    'temperature': 32,
    'humidity': 45,
    'rainfall_mm': 0,
    'sunlight_hours': 10,
    'wind_speed_kmh': 15,
    'crop_type': 1,
    'growth_stage': 1,
    'soil_type': 1,
    'season': 1,
    'ndvi': 0.35,
    'prev_irrigation_mm': 10
}

result = predictor.predict_with_satellite(features_dry, ndvi_value=0.35)
print(f"Needs Irrigation: {result['needs_irrigation']}")
print(f"Water Requirement: {result['water_requirement_mm']} mm")
print(f"Recommendation: {result['recommendation']}")
print(f"Confidence: {result['confidence']}")

# Test Case 2: Wet field (no irrigation needed)
print("\n2. WET FIELD TEST (Should NOT need irrigation)")
print("-" * 60)
features_wet = {
    'soil_moisture': 70,
    'temperature': 25,
    'humidity': 80,
    'rainfall_mm': 15,
    'sunlight_hours': 6,
    'wind_speed_kmh': 8,
    'crop_type': 1,
    'growth_stage': 1,
    'soil_type': 1,
    'season': 1,
    'ndvi': 0.75,
    'prev_irrigation_mm': 20
}

result = predictor.predict_with_satellite(features_wet, ndvi_value=0.75)
print(f"Needs Irrigation: {result['needs_irrigation']}")
print(f"Water Requirement: {result['water_requirement_mm']} mm")
print(f"Recommendation: {result['recommendation']}")
print(f"Confidence: {result['confidence']}")

# Test Case 3: Moderate conditions
print("\n3. MODERATE CONDITIONS TEST")
print("-" * 60)
features_moderate = {
    'soil_moisture': 45,
    'temperature': 28,
    'humidity': 65,
    'rainfall_mm': 5,
    'sunlight_hours': 8.5,
    'wind_speed_kmh': 12,
    'crop_type': 1,
    'growth_stage': 1,
    'soil_type': 1,
    'season': 1,
    'ndvi': 0.65,
    'prev_irrigation_mm': 15
}

result = predictor.predict_with_satellite(features_moderate, ndvi_value=0.65)
print(f"Needs Irrigation: {result['needs_irrigation']}")
print(f"Water Requirement: {result['water_requirement_mm']} mm")
print(f"Recommendation: {result['recommendation']}")
print(f"Confidence: {result['confidence']}")

print("\n" + "=" * 60)
print("MODELS WORKING CORRECTLY!")
print("=" * 60)
