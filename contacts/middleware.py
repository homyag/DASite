import json
import requests
from django.conf import settings
from django.http import JsonResponse

class RecaptchaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем только POST-запросы к contact_submit_view
        if request.method == 'POST' and request.path == '/contact/submit/':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            
            if not recaptcha_response:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'captcha': ['Обязательное поле.']
                    }
                })

            # Проверяем reCAPTCHA через Google API
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            
            try:
                response = requests.post(
                    'https://www.google.com/recaptcha/api/siteverify',
                    data=data
                )
                result = response.json()
                
                if not result.get('success'):
                    return JsonResponse({
                        'success': False,
                        'errors': {
                            'captcha': ['Неверная reCAPTCHA. Пожалуйста, попробуйте еще раз.']
                        }
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'captcha': ['Ошибка при проверке reCAPTCHA. Пожалуйста, попробуйте позже.']
                    }
                })

        return self.get_response(request) 