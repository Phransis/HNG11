import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class UserInfoView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.username('username')
        if not username:
            return JsonResponse({'error': 'username is required'}, status = 400)
        
        ip_address = self.get_client_ip(request)
        city = self.get_client_city(ip_address)
        temperature = self.get_temperature(city)

        return JsonResponse({
            'username': username,
            'ip_address': ip_address,
            'city': city,
            'temperature': temperature
        })
    

    def get_client_ip(self, request):
        x_forwaded_for = request.META.get('HTTP_X_FORARDED_FOR')
        if x_forwaded_for:
            ip = x_forwaded_for.split(',')[0]
            print(x_forwaded_for)
            print(ip)
        else:
            ip = request.META.get('REMOTE ADDR')
        return ip
    

    def get_client_city(self, ip_address):
        response = requests.get(f'https://ipapi.co/{ip_address}/json')
        data = response.json()
        return data.get('city', 'Unknown')
    

    def get_temperature(self, city):
        api_key = "03f114d4d1e883853e7858c938a1d4a1"
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid{api_key}&units=metric')
        data = response.json()
        if response.status_code == 200:
            return data['main']['temp']
        return 'Unknown'

