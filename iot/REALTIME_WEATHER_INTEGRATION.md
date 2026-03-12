# Real-Time Weather Integration Guide

## Overview

The irrigation schedule system now supports **real-time weather data** from the Open-Meteo API. This ensures irrigation schedules are based on actual weather forecasts rather than manual input.

## How It Works

### Two Modes of Operation

**Mode 1: Real-Time Weather API (Recommended)**
- Provide field coordinates (latitude, longitude)
- System automatically fetches weather data from Open-Meteo API
- Generates schedule based on actual forecasts

**Mode 2: Manual Weather Input**
- Provide 7-day rain forecast manually
- Useful for testing or when API is unavailable

## API Endpoints

### POST `/api/v1/schedule/weekly-plan`

**With Real-Time Weather:**
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

**With Manual Weather:**
```bash
curl -X POST "http://localhost:8000/api/v1/schedule/weekly-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "Wheat",
    "growth_stage": "Development",
    "current_moisture": 35.0,
    "ndvi_index": 0.65,
    "weekly_rain_forecast": [2.0, 0.5, 0.0, 3.5, 1.0, 0.0, 0.0],
    "soil_type": "loamy",
    "field_area_hectare": 2.5
  }'
```

### POST `/api/v1/schedule/daily-recommendation`

**With Real-Time Weather:**
```bash
curl -X POST "http://localhost:8000/api/v1/schedule/daily-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "Wheat",
    "growth_stage": "Development",
    "current_moisture": 35.0,
    "ndvi_index": 0.65,
    "latitude": 28.7041,
    "longitude": 77.1025
  }'
```

## Weather Data Source

**Open-Meteo API**
- Free, no API key required
- Provides 7-day weather forecast
- Includes: temperature, humidity, wind speed, precipitation
- Coverage: Global
- URL: https://api.open-meteo.com/v1/forecast

## Response Format

```json
{
  "status": "success",
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
        "reason": "...",
        "confidence": "high"
      }
    ],
    "risk_assessment": {...},
    "summary": "...",
    "key_factors": [...]
  },
  "weather_source": "Real-time API",
  "generated_at": "2026-03-12T14:30:00"
}
```

## Features

✅ **Automatic Weather Fetching**
- Provide coordinates, system fetches weather
- No manual weather input needed

✅ **Fallback Support**
- If API unavailable, use manual forecast
- Graceful degradation

✅ **Weather Source Tracking**
- Response indicates if real-time or manual
- Transparency in data source

✅ **Global Coverage**
- Works for any latitude/longitude
- No geographic restrictions

## Testing

Run the real-time weather test:
```bash
python test_realtime_weather.py
```

This will:
1. Fetch real weather for Delhi, India (28.7041, 77.1025)
2. Generate irrigation schedule based on actual forecast
3. Display daily recommendations with weather data

## Supported Locations

Any location worldwide with coordinates:
- **Delhi, India**: 28.7041, 77.1025
- **New York, USA**: 40.7128, -74.0060
- **London, UK**: 51.5074, -0.1278
- **Tokyo, Japan**: 35.6762, 139.6503
- **Sydney, Australia**: -33.8688, 151.2093

## Implementation Details

### Weather Service (`app/services/weather.py`)
- Fetches current and forecast data
- Extracts temperature, humidity, wind, precipitation
- Returns structured weather data

### Schedule Advisor (`app/services/schedule_advisor.py`)
- Accepts latitude/longitude parameters
- Calls weather service if coordinates provided
- Falls back to manual forecast if needed
- Generates schedule with weather data

### API Layer (`app/api/schedule.py`)
- Accepts optional latitude/longitude
- Validates inputs
- Routes to schedule advisor
- Returns weather source in response

## Error Handling

**No Coordinates Provided:**
- Uses manual forecast if provided
- Returns error if neither provided

**Weather API Unavailable:**
- Falls back to manual forecast
- Logs warning
- Continues with available data

**Invalid Coordinates:**
- Returns error message
- Suggests valid format

## Performance

- Weather API call: ~500ms
- Schedule generation: ~5-10s (Groq API)
- Total response time: ~6-11s

## Future Enhancements

1. **Caching**: Cache weather data for 1-2 hours
2. **Multiple APIs**: Support Weather.com, NOAA, etc.
3. **Historical Data**: Use past weather patterns
4. **Alerts**: Notify on extreme weather
5. **Satellite Integration**: Combine with satellite imagery

## Troubleshooting

**Weather data not fetching:**
- Check internet connection
- Verify coordinates are valid
- Check Open-Meteo API status

**Schedule seems incorrect:**
- Verify current_moisture value
- Check NDVI index is 0-1
- Ensure crop_type is valid

**API timeout:**
- Increase timeout in schedule_advisor.py
- Check network latency
- Try manual forecast as fallback
