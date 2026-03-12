#!/usr/bin/env python3
"""
Complete system test: ML models + Groq AI schedule generation
Shows irrigation prediction, water requirement, and weekly schedule with explanations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.prediction import predictor
from app.services.schedule_advisor import schedule_advisor

print("=" * 100)
print("COMPLETE IRRIGATION AI SYSTEM - ML Models + Groq AI Schedule")
print("=" * 100)

# Test scenario
crop_type = "Wheat"
growth_stage = "Development"
current_moisture = 35.0
ndvi_index = 0.65
weekly_rain = [2.0, 0.5, 0.0, 3.5, 1.0, 0.0, 0.0]
soil_type = "loamy"
field_area = 2.5

print(f"\nFIELD INFORMATION:")
print(f"  Crop Type: {crop_type}")
print(f"  Growth Stage: {growth_stage}")
print(f"  Soil Type: {soil_type}")
print(f"  Field Area: {field_area} hectares")
print(f"  Current Soil Moisture: {current_moisture}%")
print(f"  NDVI (Crop Health): {ndvi_index:.2f}")
print(f"  Weekly Rain Forecast: {sum(weekly_rain):.1f}mm total")

# Step 1: ML Model Predictions
print(f"\n{'=' * 100}")
print("STEP 1: ML MODEL PREDICTIONS")
print(f"{'=' * 100}")

features = {
    'soil_type': 1,
    'soil_moisture': current_moisture,
    'temperature': 28.0,
    'humidity': 65.0,
    'rainfall_mm': 5.0,
    'sunlight_hours': 8.5,
    'wind_speed_kmh': 12.0,
    'crop_type': 1,
    'growth_stage': 1,
    'season': 1,
    'ndvi': ndvi_index,
    'prev_irrigation_mm': 15.0
}

# Get ML predictions
irrigation_result = predictor.predict_irrigation_need(features)
water_requirement = predictor.predict_water_requirement(features)

print(f"\nIrrigation Model Prediction:")
print(f"  Decision: {irrigation_result.get('prediction')}")
print(f"  Needs Irrigation: {irrigation_result.get('needs_irrigation')}")
print(f"  Confidence: {irrigation_result.get('confidence'):.1%}")

print(f"\nWater Requirement Model Prediction:")
print(f"  Water Needed: {water_requirement:.2f} mm")

# Feature analysis
print(f"\nFactor Analysis (Why this decision):")
feature_analysis = irrigation_result.get('feature_analysis', {})
for factor_name, factor_data in feature_analysis.items():
    print(f"  {factor_name.upper()}: {factor_data.get('status')}")

# Step 2: Groq AI Schedule Generation
print(f"\n{'=' * 100}")
print("STEP 2: GROQ AI WEEKLY SCHEDULE GENERATION")
print(f"{'=' * 100}")

schedule_result = schedule_advisor.generate_weekly_schedule(
    crop_type=crop_type,
    growth_stage=growth_stage,
    current_moisture=current_moisture,
    ndvi_index=ndvi_index,
    weekly_rain_forecast=weekly_rain,
    soil_type=soil_type,
    field_area_hectare=field_area
)

if schedule_result.get('status') == 'success':
    schedule = schedule_result.get('schedule', {})
    
    # Next irrigation alert
    print(f"\nNEXT IRRIGATION ALERT:")
    print(f"  Date: {schedule.get('next_irrigation_date')}")
    print(f"  Day: {schedule.get('next_irrigation_day')}")
    print(f"  Water Amount: {schedule.get('next_irrigation_water_mm')}mm")
    
    # Daily schedule
    print(f"\nDAILY IRRIGATION SCHEDULE:")
    print(f"{'-' * 100}")
    
    for day_schedule in schedule.get('schedule', []):
        day = day_schedule.get('day')
        date = day_schedule.get('date')
        irrigate = day_schedule.get('irrigate')
        water = day_schedule.get('water_amount_mm')
        reason = day_schedule.get('reason')
        confidence = day_schedule.get('confidence')
        
        status = "IRRIGATE" if irrigate else "NO IRRIGATION"
        print(f"\n{day} ({date}) - {status}")
        print(f"  Confidence: {confidence}")
        if irrigate:
            print(f"  Water: {water}mm")
        print(f"  Reason: {reason[:80]}...")
    
    # Summary and recommendations
    print(f"\n{'=' * 100}")
    print("SUMMARY & RECOMMENDATIONS")
    print(f"{'=' * 100}")
    
    print(f"\nSummary:")
    print(f"  {schedule.get('summary', 'N/A')}")
    
    # Risk assessment
    risk = schedule.get('risk_assessment', {})
    print(f"\nRisk Assessment:")
    print(f"  Drought Risk: {risk.get('drought_risk', 'N/A')}")
    print(f"  Waterlogging Risk: {risk.get('waterlogging_risk', 'N/A')}")
    print(f"  Explanation: {risk.get('explanation', 'N/A')}")
    
    # Key factors
    print(f"\nKey Factors Influencing Schedule:")
    for factor in schedule.get('key_factors', []):
        print(f"  • {factor}")
    
    # Next week recommendation
    print(f"\nNext Week Recommendation:")
    print(f"  {schedule.get('next_week_recommendation', 'N/A')}")

# Step 3: Model Explanation
print(f"\n{'=' * 100}")
print("STEP 3: MODEL DECISION EXPLANATION")
print(f"{'=' * 100}")

explanation_result = schedule_advisor.generate_model_explanation(
    crop_type=crop_type,
    growth_stage=growth_stage,
    current_moisture=current_moisture,
    ndvi_index=ndvi_index,
    irrigation_prediction=irrigation_result.get('needs_irrigation', False),
    water_requirement=water_requirement,
    confidence=irrigation_result.get('confidence', 0)
)

if explanation_result.get('status') == 'success':
    explanation = explanation_result.get('explanation', {})
    
    print(f"\nModel Decision Explanation:")
    print(f"  {explanation.get('decision', 'N/A')}")
    
    print(f"\nKey Reasons:")
    for reason in explanation.get('key_reasons', []):
        print(f"  • {reason}")
    
    print(f"\nInfluential Factors:")
    factors = explanation.get('influential_factors', {})
    for factor, impact in factors.items():
        print(f"  • {factor}: {impact}")
    
    print(f"\nConcerns:")
    for concern in explanation.get('concerns', []):
        print(f"  • {concern}")
    
    print(f"\nConfidence Assessment:")
    print(f"  {explanation.get('confidence_assessment', 'N/A')}")

print(f"\n{'=' * 100}")
print("COMPLETE SYSTEM TEST FINISHED")
print(f"{'=' * 100}\n")
