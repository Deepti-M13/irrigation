import joblib
import pandas as pd
import os
import logging
import numpy as np

logger = logging.getLogger(__name__)

# Get the directory of this file and construct paths relative to it
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '../../../..'))

IRRIGATION_MODEL_PATH = os.path.join(PROJECT_ROOT, 'iot/ml_model/irrigation_model(1).pkl')
WATER_REQUIREMENT_MODEL_PATH = os.path.join(PROJECT_ROOT, 'iot/ml_model/water_requirement_model.pkl')

class IrrigationPredictor:
    def __init__(self):
        self.irrigation_model = None
        self.water_requirement_model = None
        
        # Load irrigation model
        try:
            if os.path.exists(IRRIGATION_MODEL_PATH):
                self.irrigation_model = joblib.load(IRRIGATION_MODEL_PATH)
                logger.info(f"Irrigation model loaded successfully")
            else:
                logger.warning(f"Irrigation model not found at {IRRIGATION_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Error loading irrigation model: {str(e)}")
        
        # Load water requirement model
        try:
            if os.path.exists(WATER_REQUIREMENT_MODEL_PATH):
                self.water_requirement_model = joblib.load(WATER_REQUIREMENT_MODEL_PATH)
                logger.info(f"Water requirement model loaded successfully")
            else:
                logger.warning(f"Water requirement model not found at {WATER_REQUIREMENT_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Error loading water requirement model: {str(e)}")

    def _prepare_features(self, features: dict):
        """Map input features to model feature names"""
        expected_features = ['Soil_Type', 'Soil_Moisture', 'Temperature_C', 'Humidity', 
                           'Rainfall_mm', 'Wind_Speed_kmh', 'Sunlight_Hours', 'Crop_Type', 
                           'Crop_Growth_Stage', 'Season', 'NDVI', 'Previous_Irrigation_mm']
        
        mapped_features = {
            'Soil_Type': features.get('soil_type', 1),
            'Soil_Moisture': features.get('soil_moisture', 40),
            'Temperature_C': features.get('temperature', 25),
            'Humidity': features.get('humidity', 60),
            'Rainfall_mm': features.get('rainfall_mm', 0),
            'Wind_Speed_kmh': features.get('wind_speed_kmh', 10),
            'Sunlight_Hours': features.get('sunlight_hours', 8),
            'Crop_Type': features.get('crop_type', 1),
            'Crop_Growth_Stage': features.get('growth_stage', 1),
            'Season': features.get('season', 1),
            'NDVI': features.get('ndvi', 0.5),
            'Previous_Irrigation_mm': features.get('prev_irrigation_mm', 10)
        }
        
        return pd.DataFrame([mapped_features])[expected_features], mapped_features
    
    def _get_feature_analysis(self, mapped_features: dict) -> dict:
        """Analyze features to explain irrigation decision"""
        analysis = {
            "soil_moisture": {
                "value": mapped_features.get('Soil_Moisture', 40),
                "status": self._get_moisture_status(mapped_features.get('Soil_Moisture', 40)),
                "impact": "Critical factor - directly affects irrigation need"
            },
            "ndvi": {
                "value": mapped_features.get('NDVI', 0.5),
                "status": self._get_ndvi_status(mapped_features.get('NDVI', 0.5)),
                "impact": "Indicates crop health and water stress"
            },
            "temperature": {
                "value": mapped_features.get('Temperature_C', 25),
                "status": "High" if mapped_features.get('Temperature_C', 25) > 30 else "Moderate" if mapped_features.get('Temperature_C', 25) > 20 else "Low",
                "impact": "Affects evapotranspiration rate"
            },
            "rainfall": {
                "value": mapped_features.get('Rainfall_mm', 0),
                "status": "Significant" if mapped_features.get('Rainfall_mm', 0) > 5 else "Moderate" if mapped_features.get('Rainfall_mm', 0) > 2 else "Low",
                "impact": "Reduces irrigation requirement"
            },
            "humidity": {
                "value": mapped_features.get('Humidity', 60),
                "status": "High" if mapped_features.get('Humidity', 60) > 70 else "Moderate" if mapped_features.get('Humidity', 60) > 50 else "Low",
                "impact": "Affects evaporation rate"
            }
        }
        return analysis
    
    def _get_moisture_status(self, moisture: float) -> str:
        """Get status of soil moisture"""
        if moisture < 25:
            return "Critical - Immediate irrigation needed"
        elif moisture < 40:
            return "Low - Irrigation recommended"
        elif moisture < 60:
            return "Adequate - Monitor"
        else:
            return "High - No irrigation needed"
    
    def _get_ndvi_status(self, ndvi: float) -> str:
        """Get status of NDVI"""
        if ndvi < 0.3:
            return "Severe stress - Urgent attention needed"
        elif ndvi < 0.5:
            return "Moderate stress - Needs irrigation"
        elif ndvi < 0.7:
            return "Healthy - Normal management"
        else:
            return "Very healthy - Minimal stress"
    
    def predict_irrigation_need(self, features: dict):
        """Predict if irrigation is needed (0=No, 1=Yes)"""
        if not self.irrigation_model:
            logger.warning("Irrigation model not loaded, returning default")
            return {"prediction": "Unknown", "confidence": 0.0, "needs_irrigation": False}
        
        try:
            X, mapped_features = self._prepare_features(features)
            prediction = self.irrigation_model.predict(X)[0]
            probabilities = self.irrigation_model.predict_proba(X)[0]
            confidence = max(probabilities)
            
            # Map numeric prediction to human-readable format
            irrigation_label = "Yes" if prediction == 1 else "No"
            
            # Get feature analysis for explanation
            feature_analysis = self._get_feature_analysis(mapped_features)
            
            return {
                "prediction": irrigation_label,
                "needs_irrigation": bool(prediction),
                "confidence": float(confidence),
                "raw_prediction": int(prediction),
                "feature_analysis": feature_analysis
            }
        except Exception as e:
            logger.error(f"Error during irrigation prediction: {str(e)}")
            return {"prediction": "Unknown", "confidence": 0.0, "needs_irrigation": False}
    
    def predict_water_requirement(self, features: dict):
        """Predict water requirement in mm"""
        if not self.water_requirement_model:
            logger.warning("Water requirement model not loaded, returning default")
            return 0
        
        try:
            X, _ = self._prepare_features(features)
            water_requirement = self.water_requirement_model.predict(X)[0]
            return float(water_requirement)
        except Exception as e:
            logger.error(f"Error during water requirement prediction: {str(e)}")
            return 0
    
    def predict_with_satellite(self, sensor_features: dict, ndvi_value: float = None, health_status: str = None):
        """
        Enhanced prediction incorporating satellite data
        """
        # Get irrigation need prediction
        irrigation_result = self.predict_irrigation_need(sensor_features)
        needs_irrigation = irrigation_result.get("needs_irrigation", False)
        
        # Get water requirement prediction
        water_requirement = self.predict_water_requirement(sensor_features)
        
        # Adjust based on satellite data
        if ndvi_value is not None:
            if ndvi_value < 0.3:
                needs_irrigation = True
                water_requirement *= 1.2
            elif ndvi_value > 0.75:
                needs_irrigation = False
                water_requirement *= 0.8
        
        soil_moisture = sensor_features.get("soil_moisture", 40)
        
        if ndvi_value and ndvi_value < 0.4 and soil_moisture < 30:
            final_recommendation = "Critical - Immediate irrigation needed"
        elif ndvi_value and ndvi_value < 0.5 and soil_moisture < 40:
            final_recommendation = "High - Irrigation recommended"
        elif ndvi_value and ndvi_value >= 0.7 and soil_moisture >= 50:
            final_recommendation = "Low - No irrigation needed"
        else:
            final_recommendation = "Yes - Irrigation needed" if needs_irrigation else "No - No irrigation needed"
        
        return {
            "needs_irrigation": needs_irrigation,
            "water_requirement_mm": round(water_requirement, 2),
            "recommendation": final_recommendation,
            "ndvi_factor": "Considered" if ndvi_value else "Not available",
            "ndvi_value": ndvi_value,
            "soil_moisture": soil_moisture,
            "confidence": irrigation_result.get("confidence", 0)
        }

predictor = IrrigationPredictor()
