#!/usr/bin/env python3
"""
Test irrigation prediction using trained ML models
Shows if irrigation is required and how much water is needed
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.prediction import predictor

print("=" * 80)
print("IRRIGATION PREDICTION SYSTEM - Using Trained ML Models")
print("=" * 80)

# Test scenarios
test_cases = [
    {
        "name": "Case 1: Dry Field (Critical)",
        "features": {
            'soil_type': 1,
            'soil_moisture': 20.0,  # Critical - very low
            'temperature': 32.0,
            'humidity': 45.0,
            'rainfall_mm': 0.0,
            'sunlight_hours': 10.0,
            'wind_speed_kmh': 15.0,
            'crop_type': 1,  # Wheat
            'growth_stage': 1,  # Development
            'season': 1,
            'ndvi': 0.35,  # Moderate stress
            'prev_irrigation_mm': 5.0
        }
    },
    {
        "name": "Case 2: Moderate Moisture (Normal)",
        "features": {
            'soil_type': 1,
            'soil_moisture': 45.0,  # Adequate
            'temperature': 28.0,
            'humidity': 65.0,
            'rainfall_mm': 5.0,
            'sunlight_hours': 8.5,
            'wind_speed_kmh': 12.0,
            'crop_type': 1,  # Wheat
            'growth_stage': 1,  # Development
            'season': 1,
            'ndvi': 0.65,  # Healthy
            'prev_irrigation_mm': 15.0
        }
    },
    {
        "name": "Case 3: Wet Field (No Irrigation)",
        "features": {
            'soil_type': 1,
            'soil_moisture': 70.0,  # High
            'temperature': 25.0,
            'humidity': 80.0,
            'rainfall_mm': 15.0,
            'sunlight_hours': 6.0,
            'wind_speed_kmh': 8.0,
            'crop_type': 1,  # Wheat
            'growth_stage': 1,  # Development
            'season': 1,
            'ndvi': 0.75,  # Very healthy
            'prev_irrigation_mm': 20.0
        }
    },
    {
        "name": "Case 4: Hot Day (High Evaporation)",
        "features": {
            'soil_type': 1,
            'soil_moisture': 35.0,
            'temperature': 38.0,  # Very hot
            'humidity': 35.0,  # Low humidity
            'rainfall_mm': 0.0,
            'sunlight_hours': 12.0,  # Full sun
            'wind_speed_kmh': 20.0,  # High wind
            'crop_type': 1,  # Wheat
            'growth_stage': 2,  # Mid/Late
            'season': 1,
            'ndvi': 0.60,
            'prev_irrigation_mm': 10.0
        }
    },
    {
        "name": "Case 5: Rice in Initial Stage",
        "features": {
            'soil_type': 2,  # Clay
            'soil_moisture': 30.0,
            'temperature': 30.0,
            'humidity': 70.0,
            'rainfall_mm': 2.0,
            'sunlight_hours': 8.0,
            'wind_speed_kmh': 10.0,
            'crop_type': 0,  # Rice
            'growth_stage': 0,  # Initial
            'season': 1,
            'ndvi': 0.45,
            'prev_irrigation_mm': 8.0
        }
    }
]

# Run predictions for each test case
for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST CASE {i}: {test_case['name']}")
    print(f"{'=' * 80}")
    
    features = test_case['features']
    
    # Display input parameters
    print(f"\nInput Parameters:")
    print(f"  Soil Moisture: {features['soil_moisture']}%")
    print(f"  Temperature: {features['temperature']}°C")
    print(f"  Humidity: {features['humidity']}%")
    print(f"  Rainfall Forecast: {features['rainfall_mm']}mm")
    print(f"  NDVI (Crop Health): {features['ndvi']:.2f}")
    print(f"  Wind Speed: {features['wind_speed_kmh']} km/h")
    print(f"  Sunlight Hours: {features['sunlight_hours']}h")
    
    # Get irrigation prediction
    irrigation_result = predictor.predict_irrigation_need(features)
    
    # Get water requirement prediction
    water_requirement = predictor.predict_water_requirement(features)
    
    print(f"\n{'=' * 80}")
    print(f"PREDICTION RESULTS:")
    print(f"{'=' * 80}")
    
    needs_irrigation = irrigation_result.get('needs_irrigation', False)
    prediction = irrigation_result.get('prediction', 'Unknown')
    confidence = irrigation_result.get('confidence', 0)
    
    print(f"\n🌾 IRRIGATION REQUIRED: {prediction}")
    print(f"   Confidence: {confidence:.1%}")
    
    if needs_irrigation:
        print(f"\n💧 WATER REQUIREMENT: {water_requirement:.2f} mm")
        print(f"   Status: IRRIGATION NEEDED")
    else:
        print(f"\n💧 WATER REQUIREMENT: {water_requirement:.2f} mm")
        print(f"   Status: NO IRRIGATION NEEDED")
    
    # Display feature analysis
    feature_analysis = irrigation_result.get('feature_analysis', {})
    
    print(f"\n{'=' * 80}")
    print(f"FACTOR ANALYSIS:")
    print(f"{'=' * 80}")
    
    for factor_name, factor_data in feature_analysis.items():
        value = factor_data.get('value')
        status = factor_data.get('status')
        impact = factor_data.get('impact')
        
        print(f"\n  {factor_name.upper()}:")
        print(f"    Value: {value}")
        print(f"    Status: {status}")
        print(f"    Impact: {impact}")
    
    # Recommendation
    print(f"\n{'=' * 80}")
    print(f"RECOMMENDATION:")
    print(f"{'=' * 80}")
    
    if needs_irrigation:
        print(f"\n✓ IRRIGATE THE FARM")
        print(f"  Water Amount: {water_requirement:.2f} mm")
        print(f"  Confidence Level: {confidence:.1%}")
        
        if water_requirement > 30:
            print(f"  Priority: HIGH - Significant water deficit")
        elif water_requirement > 20:
            print(f"  Priority: MEDIUM - Moderate water deficit")
        else:
            print(f"  Priority: LOW - Minor water deficit")
    else:
        print(f"\n✗ DO NOT IRRIGATE")
        print(f"  Reason: Soil moisture is adequate")
        print(f"  Confidence Level: {confidence:.1%}")

print(f"\n\n{'=' * 80}")
print("PREDICTION TESTING COMPLETE")
print(f"{'=' * 80}\n")
