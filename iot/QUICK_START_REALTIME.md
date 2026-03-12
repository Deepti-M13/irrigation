# Quick Start: Real-Time Weather Mode

## Get Irrigation Schedule with Real-Time Weather

### Step 1: Get Your Field Coordinates

Find your field's latitude and longitude:
- Google Maps: Right-click on location → Copy coordinates
- GPS Device: Read directly from device
- Online Tools: latlong.net

**Example Coordinates:**
- Delhi, India: 28.7041, 77.1025
- New York, USA: 40.7128, -74.0060
- London, UK: 51.5074, -0.1278

### Step 2: Call the API

```bash
curl -X POST "http://localhost:8000/api/v1/schedule/weekly-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "Wheat",
    "growth_stage": "Development",
    "current_moisture": 35.0,
    "ndvi_index": 0.65,
    "latitude": 28.7041,
    "longitude": 77.1025,
    "soil_type": "loamy",
    "field_area_hectare": 2.5
  }'
```

### Step 3: Get Results

Response includes:
- **Next irrigation date** (e.g., 2026-03-14)
- **Daily schedule** for 7 days
- **Water requirements** in mm
- **Risk assessment** (drought/waterlogging)
- **Weather source**: "Real-time API"

## What Happens Behind the Scenes

1. **Coordinates Provided** → System fetches real weather
2. **Weather Data Retrieved** → From Open-Meteo API
3. **ML Models Predict** → Irrigation need + water requirement
4. **Groq AI Generates** → Weekly schedule with explanations
5. **Schedule Returned** → With dates and recommendations

## Example Response

```json
{
  "status": "success",
  "weather_source": "Real-time API",
  "schedule": {
    "next_irrigation_date": "2026-03-14",
    "next_irrigation_day": "Wednesday",
    "next_irrigation_water_mm": 4,
    "schedule": [
      {
        "day": "Monday",
        "date": "2026-03-12",
        "irrigate": false,
        "water_amount_mm": 0,
        "reason": "Soil moisture is adequate...",
        "confidence": "high"
      },
      {
        "day": "Wednesday",
        "date": "2026-03-14",
        "irrigate": true,
        "water_amount_mm": 4,
        "reason": "No rain forecasted...",
        "confidence": "high"
      }
    ],
    "risk_assessment": {
      "drought_risk": "low",
      "waterlogging_risk": "low"
    },
    "summary": "Irrigation needed on Wednesday..."
  }
}
```

## Parameters Explained

| Parameter | Required | Example | Notes |
|-----------|----------|---------|-------|
| crop_type | Yes | "Wheat" | Rice, Wheat, Maize, Cotton, Pulse |
| growth_stage | Yes | "Development" | Initial, Development, Mid/Late |
| current_moisture | Yes | 35.0 | 0-100% |
| ndvi_index | Yes | 0.65 | 0-1 (0=dead, 1=healthy) |
| latitude | Yes* | 28.7041 | Field latitude |
| longitude | Yes* | 77.1025 | Field longitude |
| soil_type | No | "loamy" | Sandy, Loamy, Clay, Silty |
| field_area_hectare | No | 2.5 | Field size in hectares |

*Required for real-time weather mode

## Test It Now

```bash
cd iot/backend
python test_realtime_weather.py
```

This will:
- Fetch real weather for Delhi, India
- Generate irrigation schedule
- Show daily recommendations
- Display risk assessment

## Common Locations

```bash
# Delhi, India
latitude: 28.7041, longitude: 77.1025

# New York, USA
latitude: 40.7128, longitude: -74.0060

# London, UK
latitude: 51.5074, longitude: -0.1278

# Tokyo, Japan
latitude: 35.6762, longitude: 139.6503

# Sydney, Australia
latitude: -33.8688, longitude: 151.2093
```

## What You Get

✅ **Irrigation Schedule** - When to irrigate each day
✅ **Water Requirements** - How much water in mm
✅ **Next Irrigation Alert** - Exact date and time
✅ **Risk Assessment** - Drought and waterlogging risks
✅ **AI Explanations** - Why each decision was made
✅ **Real-Time Weather** - Based on actual forecasts

## Troubleshooting

**"Weather source: Manual forecast"**
- Coordinates not provided or invalid
- Provide valid latitude/longitude

**"Status: error"**
- Check all required parameters
- Verify crop_type and growth_stage are valid
- Ensure current_moisture is 0-100

**Slow response (>15 seconds)**
- Weather API might be slow
- Groq API processing time
- Normal for first request

## Next Steps

1. Get your field coordinates
2. Call the API with real-time mode
3. Receive irrigation schedule
4. Follow daily recommendations
5. Monitor soil moisture
6. Adjust as needed

## Support

For issues:
- Check REALTIME_WEATHER_INTEGRATION.md
- Review API response status
- Verify coordinates format
- Check internet connection
