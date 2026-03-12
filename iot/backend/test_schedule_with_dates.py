#!/usr/bin/env python3
"""
Test schedule advisor with date and next irrigation time display
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.schedule_advisor import schedule_advisor
from datetime import datetime

print("=" * 80)
print("Testing Weekly Schedule with Dates and Next Irrigation Time")
print("=" * 80)

weekly_rain = [2.0, 0.5, 0.0, 3.5, 1.0, 0.0, 0.0]

schedule_result = schedule_advisor.generate_weekly_schedule(
    crop_type="Wheat",
    growth_stage="Development",
    current_moisture=35.0,
    ndvi_index=0.65,
    weekly_rain_forecast=weekly_rain,
    soil_type="loamy",
    field_area_hectare=2.5
)

print(f"\nStatus: {schedule_result.get('status')}")
print(f"Generated at: {schedule_result.get('generated_at')}")

if schedule_result.get('status') == 'success':
    schedule = schedule_result.get('schedule', {})
    
    print("\n" + "=" * 80)
    print("WEEKLY IRRIGATION SCHEDULE")
    print("=" * 80)
    
    # Display next irrigation info
    next_date = schedule.get('next_irrigation_date', 'N/A')
    next_day = schedule.get('next_irrigation_day', 'N/A')
    next_water = schedule.get('next_irrigation_water_mm', 0)
    
    print(f"\n🚨 NEXT IRRIGATION REQUIRED:")
    print(f"   Date: {next_date}")
    print(f"   Day: {next_day}")
    print(f"   Water Amount: {next_water}mm")
    
    # Display daily schedule with dates
    print(f"\n📅 DAILY SCHEDULE:")
    print("-" * 80)
    
    for day_schedule in schedule.get('schedule', []):
        day = day_schedule.get('day', 'N/A')
        date = day_schedule.get('date', 'N/A')
        irrigate = day_schedule.get('irrigate', False)
        water = day_schedule.get('water_amount_mm', 0)
        reason = day_schedule.get('reason', 'N/A')
        confidence = day_schedule.get('confidence', 'N/A')
        
        status = "✓ IRRIGATE" if irrigate else "✗ NO IRRIGATION"
        
        print(f"\n{day} ({date})")
        print(f"  Status: {status}")
        if irrigate:
            print(f"  Water: {water}mm")
        print(f"  Confidence: {confidence}")
        print(f"  Reason: {reason[:70]}...")
    
    # Display summary
    print(f"\n" + "=" * 80)
    print("SUMMARY & RECOMMENDATIONS")
    print("=" * 80)
    
    print(f"\nSummary: {schedule.get('summary', 'N/A')}")
    
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

print("\n" + "=" * 80)
print("Test Complete!")
print("=" * 80)
