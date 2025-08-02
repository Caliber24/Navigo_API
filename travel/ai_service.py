import requests
from django.conf import settings

HF_API_URL = "https://api-inference.huggingface.co/models/HooshvareLab/gpt2-fa"
headers = {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}


class AIRecommender:
    @staticmethod
    def refine_itinerary(destination, raw_itinerary, styles, daily_budget):
        prompt = (
            f"سبک سفرها: {styles}\n"
            f"بودجه روزانه: {daily_budget} تومان\n"
            f"مقصد: {destination}\n"
            f"برنامه‌ی اولیه سفر:\n{raw_itinerary}\n\n"
            f"لطفاً این برنامه را به شکل حرفه‌ای و با نکات محلی، رستوران‌های پیشنهادی و برنامه‌ریزی زمانی به زبان فارسی تکمیل کن."
        )
        
        payload = {
          "inputs": prompt,
          "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
          }
        }
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        output = response.json()
        
        if isinstance(output, list) and 'generated_text' in output[0]:
          return output[0]['generated_text']
        return output.get('generated_text', '')
