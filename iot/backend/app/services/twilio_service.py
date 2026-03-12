from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Twilio credentials should be in .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Language mapping for Twilio <Say>
# Using specific Polly voices for Indian languages where supported
LANGUAGE_MAP = {
    "English": {"lang": "en-IN", "voice": "Polly.Raveena"},
    "Hindi": {"lang": "hi-IN", "voice": "Polly.Aditi"},
    "Telugu": {"lang": "te-IN", "voice": "Polly.Chitra"},
    "Tamil": {"lang": "ta-IN", "voice": "Polly.Vani"},
    "Kannada": {"lang": "kn-IN", "voice": "Polly.Hiya"},
    "Marathi": {"lang": "mr-IN", "voice": "Polly.Aditi"},
    "Bengali": {"lang": "bn-IN", "voice": "Polly.Aditi"},
    "Gujarati": {"lang": "gu-IN", "voice": "Polly.Aditi"},
    "Malayalam": {"lang": "ml-IN", "voice": "Polly.Aditi"}
}

# Centralized mapping for speech recognition
SPEECH_LANG_MAP = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
    "Kannada": "kn-IN",
    "Marathi": "mr-IN",
    "Bengali": "bn-IN",
    "Gujarati": "gu-IN",
    "Malayalam": "ml-IN"
}

class TwilioVoiceService:
    def __init__(self):
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        else:
            self.client = None
            logger.warning("Twilio credentials not found. Voice calls will be simulated.")

    def make_onboarding_call(self, to_phone: str, base_url: str):
        if not self.client:
            logger.info(f"SIMULATED ONBOARDING CALL to {to_phone}")
            return "simulated_onboarding_sid"
        
        twiml_url = f"{base_url}/api/v1/voice/language-selection"
        
        try:
            call = self.client.calls.create(
                to=to_phone,
                from_=TWILIO_PHONE_NUMBER,
                url=twiml_url
            )
            return call.sid
        except Exception as e:
            logger.error(f"Error making Twilio onboarding call: {str(e)}")
            return None

    def get_language_selection_twiml(self, base_url: str):
        response = VoiceResponse()
        gather = Gather(num_digits=1, action=f"{base_url}/api/v1/voice/save-language", method='POST', timeout=10)
        
        # Keep it SHORT to fit within trial time limit
        gather.say("English press 1.", voice="Polly.Raveena", language="en-IN")
        gather.say("हिंदी के लिए 2 दबाएं।", voice="Polly.Aditi", language="hi-IN")
        gather.say("తెలుగు కోసం 3 నొక్కండి.", voice="Polly.Chitra", language="te-IN")
        gather.say("தமிழுக்கு 4 அழுத்தவும்.", voice="Polly.Vani", language="ta-IN")
        gather.say("ಕನ್ನಡಕ್ಕಾಗಿ 5 ಒತ್ತಿರಿ.", voice="Polly.Hiya", language="kn-IN")
        gather.say("मराठीसाठी 6 दाबा.", voice="Polly.Aditi", language="mr-IN")
        gather.say("বাংলার জন্য 7 টিপুন।", voice="Polly.Aditi", language="bn-IN")
        gather.say("ગુજરાતી માટે 8 દબાવો.", voice="Polly.Aditi", language="gu-IN")
        gather.say("മലയാളത്തിനായി 9 അമർത്തുക.", voice="Polly.Aditi", language="ml-IN")
        
        response.append(gather)
        response.redirect(f"{base_url}/api/v1/voice/language-selection")
        return str(response)

    def get_advisory_twiml(self, message: str, language: str):
        response = VoiceResponse()
        lang_info = LANGUAGE_MAP.get(language, LANGUAGE_MAP["English"])
        response.say(message, voice=lang_info["voice"], language=lang_info["lang"])
        return str(response)

    def get_irrigation_alert_twiml(self, language: str):
        response = VoiceResponse()
        lang_info = LANGUAGE_MAP.get(language, LANGUAGE_MAP["English"])
        
        gather = Gather(num_digits=1, action='/api/v1/voice/handle-alert-input', method='POST')
        
        alert_texts = {
            "English": "Soil moisture is still low. Press 1 to continue irrigation. Press 2 to stop irrigation.",
            "Hindi": "मिट्टी की नमी अभी भी कम है। सिंचाई जारी रखने के लिए 1 दबाएं। रोकने के लिए 2 दबाएं।",
            "Telugu": "నేల తేమ ఇంకా తక్కువగా ఉంది. సాగును కొనసాగించడానికి 1 నొక్కండి. నిలిపివేయడానికి 2 నొక్కండి.",
            "Tamil": "மண் ஈரப்பதம் ఇంకా குறைவாக உள்ளது. நீர்ப்பாசனத்தைத் தொடர 1 ஐ அழுத்தவும். நிறுத்த 2 ஐ அழுத்தவும்.",
            "Kannada": "ಮಣ್ಣಿನ ತೇವಾಂಶ ಇನ್ನೂ ಕಡಿಮೆಯಿದೆ. ನೀರಾವರಿ ಮುಂದುವರಿಸಲು 1 ಒತ್ತಿರಿ. ನಿಲ್ಲಿಸಲು 2 ಒತ್ತಿರಿ.",
            "Marathi": "जमिनीतील ओलावा अजूनही कमी आहे. सिंचन सुरू ठेवण्यासाठी 1 दाबा. थांबवण्यासाठी 2 दाबा.",
            "Bengali": "মাটির আর্দ্রতা এখনও কম। সেচ চালিয়ে যেতে 1 টিপুন। বন্ধ করতে 2 টিপুন।",
            "Gujarati": "જમીનનો ભેજ હજુ ઓછો છે. સિંચાઈ ચાલુ રાખવા માટે 1 દબાવો. બંધ કરવા માટે 2 દબાવો।",
            "Malayalam": "മണ്ണ് ഈർപ്പം ഇപ്പോഴും കുറവാണ്. ജലസേചനം തുടരാൻ 1 അമർത്തുക. നിർത്താൻ 2 അമർത്തുക."
        }
        
        text = alert_texts.get(language, alert_texts["English"])
        gather.say(text, voice=lang_info["voice"], language=lang_info["lang"])
        response.append(gather)
        return str(response)

twilio_service = TwilioVoiceService()
