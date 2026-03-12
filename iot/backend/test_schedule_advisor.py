#!/usr/bin/env python3
"""
Test script for the Groq-powered schedule advisor
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.schedule_advisor import schedule_advisor
from app.services.prediction import predictor

print("=" * 70)
print("Testing Groq-Powered Schedule Advisor")
print("=" * 70)

# Test 1: Weekly Schedule Generation
print("\n1. Testing Weekly Schedule Generation:")
print("-" * 70)

weekly_rain = [2.0, 0.5, 0.0, 3.5, 1.0, 0.0, 0.0]  # mm for each day

schedule_result = schedule_advisor.generate_weekly_schedule(
    crop_type="Wheat",
    growth_stage="Development",
    current_moisture=35.0,
    ndvi_index=0.65,
    weekly_rain_forecast=weekly_rain,
    soil_type="loamy",
    field_area_hectare=2.5
)

print(f"Status: {schedule_result.get('status')}")
if schedule_result.get('status') == 'success':
    schedule = schedule_result.get('schedule', {})
    print(f"\nGenerated Schedule:")
    print(f"Summary: {schedule.get('summary', 'N/A')}")
    print(f"\nDaily Schedule:")
    for day in schedule.get('schedule', []):
        print(f"  {day.get('day')}: Irrigate={day.get('irrigate')} | "
              f"Water={day.get('water_amount_mm', 0)}mm | "
              f"Reason: {day.get('reason', 'N/A')}")
    
    print(f"\nKey Factors:")
    for factor in schedule.get('key_factors', []):
        print(f"  - {factor}")
    
    print(f"\nRisk Assessment:")
    risk = schedule.get('risk_assessment', {})
    print(f"  Drought Risk: {risk.get('drought_risk', 'N/A')}")
    print(f"  Waterlogging Risk: {risk.get('waterlogging_risk', 'N/A')}")
    print(f"  Explanation: {risk.get('explanation', 'N/A')}")
    
    print(f"\nNext Week Recommendation:")
    print(f"  {schedule.get('next_week_recommendation', 'N/A')}")
else:
    print(f"Error: {schedule_result.get('message', 'Unknown error')}")

# Test 2: Model Explanation
print("\n\n2. Testing Model Explanation:")
print("-" * 70)

explanation_result = schedule_advisor.generate_model_explanation(
    crop_type="Wheat",
    growth_stage="Development",
    current_moisture=35.0,
    ndvi_index=0.65,
    irrigation_prediction=True,
    water_requirement=25.5,
    confidence=0.95
)

print(f"Status: {explanation_result.get('status')}")
if explanation_result.get('status') == 'success':
    explanation = explanation_result.get('explanation', {})
    print(f"\nModel Decision: {explanation.get('decision', 'N/A')}")
    print(f"\nKey Reasons:")
    for reason in explanation.get('key_reasons', []):
        print(f"  - {reason}")
    
    print(f"\nInfluential Factors:")
    factors = explanation.get('influential_factors', {})
    for factor, impact in factors.items():
        print(f"  - {factor}: {impact}")
    
    print(f"\nConcerns:")
    for concern in explanation.get('concerns', []):
        print(f"  - {concern}")
    
    print(f"\nConfidence Assessment:")
    print(f"  {explanation.get('confidence_assessment', 'N/A')}")
else:
    print(f"Error: {explanation_result.get('message', 'Unknown error')}")

# Test 3: Different Scenarios
print("\n\n3. Testing Different Scenarios:")
print("-" * 70)

scenarios = [
    {
        "name": "Dry conditions with low NDVI",
        "crop_type": "Rice",
        "growth_stage": "Mid/Late",
        "moisture": 20.0,
        "ndvi": 0.35,
        "rain": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
        "name": "Wet conditions with high NDVI",
        "crop_type": "Maize",
        "growth_stage": "Development",
        "moisture": 65.0,
        "ndvi": 0.75,
        "rain": [5.0, 3.0, 2.0, 1.0, 0.0, 0.0, 0.0]
    },
    {
        "name": "Initial stage with moderate conditions",
        "crop_type": "Cotton",
        "growth_stage": "Initial",
        "moisture": 45.0,
        "ndvi": 0.50,
        "rain": [1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
]

for scenario in scenarios:
    print(f"\nScenario: {scenario['name']}")
    print(f"  Crop: {scenario['crop_type']}, Stage: {scenario['growth_stage']}")
    print(f"  Moisture: {scenario['moisture']}%, NDVI: {scenario['ndvi']}")
    
    result = schedule_advisor.generate_weekly_schedule(
        crop_type=scenario['crop_type'],
        growth_stage=scenario['growth_stage'],
        current_moisture=scenario['moisture'],
        ndvi_index=scenario['ndvi'],
        weekly_rain_forecast=scenario['rain']
    )
    
    if result.get('status') == 'success':
        schedule = result.get('schedule', {})
        print(f"  Summary: {schedule.get('summary', 'N/A')[:100]}...")
    else:
        print(f"  Error: {result.get('message', 'Unknown error')}")

print("\n" + "=" * 70)
print("Schedule Advisor Testing Complete!")
print("=" * 70)
