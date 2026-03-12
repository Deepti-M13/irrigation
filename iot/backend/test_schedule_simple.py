#!/usr/bin/env python3
"""
Simple test for schedule advisor with mock data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.prediction import predictor

print("=" * 70)
print("Testing Irrigation Prediction with Feature Analysis")
print("=" * 70)

# Test features
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
    'ndvi': 0.65,
    'prev_irrigation_mm': 15.0
}

print("\n1. Testing Prediction with Feature Analysis:")
print("-" * 70)

irrigation_result = predictor.predict_irrigation_need(test_features)

print(f"Prediction: {irrigation_result.get('prediction')}")
print(f"Needs Irrigation: {irrigation_result.get('needs_irrigation')}")
print(f"Confidence: {irrigation_result.get('confidence'):.2%}")

print(f"\nFeature Analysis:")
feature_analysis = irrigation_result.get('feature_analysis', {})
for feature, details in feature_analysis.items():
    print(f"\n  {feature.upper()}:")
    print(f"    Value: {details.get('value')}")
    print(f"    Status: {details.get('status')}")
    print(f"    Impact: {details.get('impact')}")

# Test different scenarios
print("\n\n2. Testing Different Scenarios:")
print("-" * 70)

scenarios = [
    {
        "name": "Dry conditions (critical)",
        "features": {**test_features, 'soil_moisture': 20.0, 'ndvi': 0.35}
    },
    {
        "name": "Wet conditions (adequate)",
        "features": {**test_features, 'soil_moisture': 70.0, 'ndvi': 0.75}
    },
    {
        "name": "Hot day (high evaporation)",
        "features": {**test_features, 'temperature': 38.0, 'humidity': 40.0}
    },
    {
        "name": "Rainy day (low irrigation need)",
        "features": {**test_features, 'rainfall_mm': 15.0, 'soil_moisture': 50.0}
    }
]

for scenario in scenarios:
    print(f"\nScenario: {scenario['name']}")
    result = predictor.predict_irrigation_need(scenario['features'])
    
    print(f"  Prediction: {result.get('prediction')}")
    print(f"  Confidence: {result.get('confidence'):.2%}")
    
    # Show key factors
    analysis = result.get('feature_analysis', {})
    print(f"  Key Factors:")
    print(f"    - Soil Moisture: {analysis.get('soil_moisture', {}).get('status')}")
    print(f"    - NDVI Status: {analysis.get('ndvi', {}).get('status')}")
    print(f"    - Temperature: {analysis.get('temperature', {}).get('status')}")

print("\n" + "=" * 70)
print("Feature Analysis Testing Complete!")
print("=" * 70)
