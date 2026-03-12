#!/usr/bin/env python3
"""
Test schedule generation with real-time weather API integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.schedule_advisor import schedule_advisor

print("=" * 100)
print("IRRIGATION SCHEDULE WITH REAL-TIME WEATHER API")
print("=" * 100)

# Example: Using real coordinates (Delhi, India)
latitude = 28.7041
longitude = 77.1025

print(f"\nFIELD LOCATION:")
print(f"  Latitude: {latitude}")
print(f"  Longitude: {longitude}")
print(f"  (This will fetch real-time weather data from Open-Meteo API)")

print(f"\nFIELD INFORMATION:")
print(f"  Crop Type: Wheat")
print(f"  Growth Stage: Development")
print(f"  Current Soil Moisture: 35%")
print(f"  NDVI (Crop Health): 0.65")
print(f"  Soil Type: loamy")
print(f"  Field Area: 2.5 hectares")

print(f"\n{'=' * 100}")
print("GENERATING SCHEDULE WITH REAL-TIME WEATHER DATA...")
print(f"{'=' * 100}")

# Generate schedule with real-time weather
schedule_result = schedule_advisor.generate_weekly_schedule(
    crop_type="Wheat",
    growth_stage="Development",
    current_moisture=35.0,
    ndvi_index=0.65,
    latitude=latitude,
    longitude=longitude,
    soil_type="loamy",
    field_area_hectare=2.5
)

print(f"\nStatus: {schedule_result.get('status')}")
print(f"Weather Source: {schedule_result.get('weather_source')}")
print(f"Generated at: {schedule_result.get('generated_at')}")

if schedule_result.get('status') == 'success':
    schedule = schedule_result.get('schedule', {})
    
    print(f"\n{'=' * 100}")
    print("WEEKLY IRRIGATION SCHEDULE (WITH REAL-TIME WEATHER)")
    print(f"{'=' * 100}")
    
    # Next irrigation alert
    print(f"\nNEXT IRRIGATION REQUIRED:")
    print(f"  Date: {schedule.get('next_irrigation_date')}")
    print(f"  Day: {schedule.get('next_irrigation_day')}")
    print(f"  Water Amount: {schedule.get('next_irrigation_water_mm')}mm")
    
    # Daily schedule
    print(f"\nDAILY SCHEDULE:")
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
        print(f"  Reason: {reason[:75]}...")
    
    # Summary
    print(f"\n{'=' * 100}")
    print("SUMMARY & ANALYSIS")
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
    print(f"\nKey Factors:")
    for factor in schedule.get('key_factors', []):
        print(f"  • {factor}")
    
    # Next week recommendation
    print(f"\nNext Week Recommendation:")
    print(f"  {schedule.get('next_week_recommendation', 'N/A')}")

else:
    print(f"Error: {schedule_result.get('message', 'Unknown error')}")

print(f"\n{'=' * 100}")
print("TEST COMPLETE")
print(f"{'=' * 100}\n")

print("NOTE: The schedule was generated using REAL-TIME weather data from Open-Meteo API")
print("      This ensures the irrigation schedule is based on actual weather forecasts")
print("      for the specified location (latitude, longitude)")
