# ML Models Integration Guide

## Overview

Your IoT backend now integrates two trained machine learning models:

1. **Irrigation Model** (`irrigation_model(1).pkl`) - Binary classifier predicting if irrigation is needed (Yes/No)
2. **Water Requirement Model** (`water_requirement_model.pkl`) - Regression model predicting water requirement in millimeters

## Model Locations

- `iot/ml_model/irrigation_model(1).pkl`
- `iot/ml_model/water_requirement_model.pkl`

## Model Specifications

### Irrigation Model
- **Type:** Binary Classification (Random Forest)
- **Classes:** 0 (No irrigation needed), 1 (Irrigation needed)
- **Output:** Boolean + confidence score
- **Confidence Range:** 0.0-1.0

### Water Requirement Model
- **Type:** Regression (Random Forest)
- **Output Range:** 0-100+ mm
- **Interpretation:** Recommended water amount in millimeters

## Integration Points

### 1. Prediction Service (`iot/backend/app/services/prediction.py`)

The `IrrigationPredictor` class loads and manages both models:

```python
from app.services.prediction import predictor

# Predict irrigation need
irrigation_result = predictor.predict_irrigation_need(features_dict)
# Returns: {
#   "prediction": "Yes" or "No",
#   "needs_irrigation": True/False,
#   "confidence": 0.0-1.0,
#   "raw_prediction": 0 or 1
# }

# Predict water requirement
water_requirement = predictor.predict_water_requirement(features_dict)
# Returns: float (mm)

# Combined prediction with satellite data
result = predictor.predict_with_satellite(
    sensor_features=features_dict,
    ndvi_value=0.65,
    health_status="Moderate"
)
```

### 2. Sensor API Endpoint (`iot/backend/app/api/sensors.py`)

#### POST `/sensors/data`
Receives sensor data and returns irrigation recommendation with water requirement:

```json
{
  "status": "success",
  "needs_irrigation": true,
  "irrigation_confidence": 0.95,
  "water_requirement_mm": 25.5,
  "pump_action": "START",
  "soil_moisture": 35.5,
  "temperature": 28.0,
  "humidity": 65.0
}
```

#### POST `/sensors/predict`
Direct prediction endpoint with custom parameters:

**Query Parameters:**
- `soil_type` (int): 0-5 (default: 1)
- `soil_moisture` (float): 0-100 (required)
- `temperature` (float): °C (required)
- `humidity` (float): 0-100 (required)
- `rainfall_mm` (float): mm (default: 0)
- `sunlight_hours` (float): hours (default: 8)
- `wind_speed_kmh` (float): km/h (default: 10)
- `crop_type` (int): 0-4 (default: 1)
- `growth_stage` (int): 0-2 (default: 1)
- `season` (int): 0-3 (default: 1)
- `ndvi` (float): 0-1 (default: 0.5)
- `prev_irrigation_mm` (float): mm (default: 10)

**Response:**
```json
{
  "needs_irrigation": true,
  "water_requirement_mm": 25.5,
  "confidence": 0.95,
  "input_parameters": {...}
}
```

## Required Input Features

All models expect these 12 features:

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| soil_type | int | 0-5 | Soil type classification |
| soil_moisture | float | 0-100 | Soil moisture percentage |
| temperature | float | 15-45 | Temperature in °C |
| humidity | float | 20-90 | Humidity percentage |
| rainfall_mm | float | 0-20 | Rainfall in mm |
| wind_speed_kmh | float | 5-30 | Wind speed in km/h |
| sunlight_hours | float | 4-12 | Daily sunlight hours |
| crop_type | int | 0-4 | 0: Rice, 1: Wheat, 2: Maize, 3: Cotton, 4: Pulse |
| growth_stage | int | 0-2 | 0: Initial, 1: Development, 2: Mid/Late |
| season | int | 0-3 | Season indicator |
| ndvi | float | 0-1 | Normalized Difference Vegetation Index |
| prev_irrigation_mm | float | 0-50 | Previous irrigation in mm |

## Model Outputs

### Irrigation Model
- **Output:** Binary (Yes/No)
- **Confidence:** 0.0-1.0 (probability of prediction)
- **Interpretation:** 
  - "Yes" = Irrigation is needed
  - "No" = No irrigation needed

### Water Requirement Model
- **Output:** Regression value
- **Range:** 0-100+ mm
- **Interpretation:** Recommended water amount in millimeters

## Usage Examples

### Example 1: Basic Prediction

```python
from app.services.prediction import predictor

features = {
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

# Get predictions
irrigation = predictor.predict_irrigation_need(features)
water = predictor.predict_water_requirement(features)

print(f"Needs Irrigation: {irrigation['needs_irrigation']}")
print(f"Confidence: {irrigation['confidence']:.2%}")
print(f"Water Requirement: {water:.2f} mm")
```

### Example 2: With Satellite Data

```python
result = predictor.predict_with_satellite(
    sensor_features=features,
    ndvi_value=0.65,
    health_status="Moderate"
)

print(f"Recommendation: {result['recommendation']}")
print(f"Water Requirement: {result['water_requirement_mm']} mm")
print(f"Confidence: {result['confidence']:.2%}")
```

### Example 3: API Call

```bash
curl -X POST "http://localhost:8000/sensors/predict?soil_moisture=35.5&temperature=28&humidity=65&rainfall_mm=5&sunlight_hours=8.5&wind_speed_kmh=12&crop_type=1&growth_stage=1&soil_type=1&season=1&ndvi=0.5&prev_irrigation_mm=15"
```

## Testing

Run the test script to verify models are working:

```bash
python iot/backend/test_models.py
```

Expected output shows:
- Irrigation predictions (Yes/No with confidence)
- Water requirement predictions (in mm)
- Different scenarios (dry, wet, hot, cool conditions)

## Troubleshooting

### Models Not Loading

**Error:** "Model not found at..."
- **Solution:** Ensure model files are in `iot/ml_model/` directory
- Check file names match exactly: `irrigation_model(1).pkl` and `water_requirement_model.pkl`

### Feature Mismatch

**Error:** "The feature names should match those that were passed during fit"
- **Solution:** Ensure all 12 required features are provided with correct names
- Use the `_prepare_features()` method which handles feature mapping

### Scikit-learn Version Warnings

**Warning:** "Trying to unpickle estimator from version X when using version Y"
- **Solution:** This is a compatibility warning but models still work
- To fix: Retrain models with current scikit-learn version

## Model Performance

- **Irrigation Model:** Random Forest Classifier (100 estimators)
- **Water Requirement Model:** Random Forest Regressor
- **Training Data:** 200,000+ synthetic samples
- **Accuracy:** Varies based on input data distribution

## Integration Checklist

- [x] Models loaded in prediction service
- [x] Feature mapping implemented
- [x] Sensor API endpoint updated
- [x] New prediction endpoint created
- [x] Satellite data integration
- [x] Error handling and logging
- [x] Test script created and verified
- [ ] Deploy to production
- [ ] Monitor model performance
- [ ] Collect real-world feedback
- [ ] Retrain with real field data

## Next Steps

1. **Deploy to production:**
   ```bash
   pip install -r iot/backend/requirements.txt
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Test endpoints:**
   - POST `/sensors/data` with sensor readings
   - POST `/sensors/predict` with custom parameters

3. **Monitor predictions:**
   - Track model accuracy over time
   - Collect feedback from farmers
   - Identify edge cases

4. **Future improvements:**
   - Retrain with real field data
   - Add more features (soil type, crop variety, etc.)
   - Implement model versioning
   - Create model performance dashboard
