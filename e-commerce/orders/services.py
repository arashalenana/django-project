import requests
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

def make_payment(phone, amount):
    url= f"{os.environ.get('FASTAPI_URL')}/api/v1/stkpush"
    payload = {
        "phone": phone,
        "amount": amount
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    # print(response.json())  # For debugging purposes
    return response.json()


@csrf_exempt
def confirm_payment(request):
    url = f"{os.environ.get('FASTAPI_URL')}/api/v1/callback"
    try:
        response = requests.post(url, data=request.body, headers={'Content-Type': 'application/json'})
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        # Handle the exception (e.g., log it, return an error response, etc.)
        return JsonResponse({'error': f'Error confirming payment: {e}'}, status=500)