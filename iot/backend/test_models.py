#!/usr/bin/env python3
"""
Test script to verify the trained models are working correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.prediction import predictor

# Test data with correct feature names
test_features = {
    'soil_type': 1,
    'soil_moisture': 35.5,
    'temperature': 28.0,
    'humidity': 65.0,
    'rainfall_mm': 5.0,
    'sunlight_hours': 8.5,
    'wind_speed_kmh': 12.0,
    'crop_type': 1,
    'growth_stage': 1,
    'season': 1,
    'ndvi': 0.5,
    'prev_irrigation_mm': 15.0
}

print("=" * 60)
print("Testing Trained Models")
print("=" * 60)

# Test 1: Irrigation Need Prediction
print("\n1. Testing Irrigation Need Prediction:")
print("-" * 40)
irrigation_result = predictor.predict_irrigation_need(test_features)
print(f"Input features: {test_features}")
print(f"Result: {irrigation_result}")
print(f"Needs Irrigation: {irrigation_result.get('needs_irrigation')}")
print(f"Confidence: {irrigation_result.get('confidence'):.2%}")

# Test 2: Water Requirement Prediction
print("\n2. Testing Water Requirement Prediction:")
print("-" * 40)
water_req = predictor.predict_water_requirement(test_features)
print(f"Water Requirement: {water_req} mm")

# Test 3: Combined Prediction with Satellite Data
print("\n3. Testing Combined Prediction with Satellite Data:")
print("-" * 40)
combined_result = predictor.predict_with_satellite(
    test_features,
    ndvi_value=0.65,
    health_status="Moderate"
)
print(f"Combined Result:")
for key, value in combined_result.items():
    print(f"  {key}: {value}")

# Test 4: Different scenarios
print("\n4. Testing Different Scenarios:")
print("-" * 40)

scenarios = [
    {
        "name": "Dry conditions (low moisture)",
        "features": {**test_features, 'soil_moisture': 20.0, 'rainfall_mm': 0.0}
    },
    {
        "name": "Wet conditions (high moisture)",
        "features": {**test_features, 'soil_moisture': 70.0, 'rainfall_mm': 15.0}
    },
    {
        "name": "Hot day (high temp)",
        "features": {**test_features, 'temperature': 38.0, 'humidity': 40.0}
    },
    {
        "name": "Cool day (low temp)",
        "features": {**test_features, 'temperature': 18.0, 'humidity': 80.0}
    }
]

for scenario in scenarios:
    print(f"\nScenario: {scenario['name']}")
    irrigation = predictor.predict_irrigation_need(scenario['features'])
    water = predictor.predict_water_requirement(scenario['features'])
    
    needs_irr = irrigation.get('needs_irrigation', False)
    confidence = irrigation.get('confidence', 0)
    
    print(f"  Needs Irrigation: {needs_irr} (confidence: {confidence:.2%})")
    print(f"  Water Requirement: {water:.2f} mm")

print("\n" + "=" * 60)
print("Model Testing Complete!")
print("=" * 60)
