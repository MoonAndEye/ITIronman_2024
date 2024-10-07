from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def hello_world(request):
    return JsonResponse({"message": "Hello, World!"})

@api_view(['POST'])
def login_view(request):
    account = request.data.get('account')
    password = request.data.get('password')

    user = authenticate(username=account, password=password)

    if user is not None:
        return JsonResponse({"message": "Login successful!"}, status=200)
    else:
        return JsonResponse({"message": "Invalid credentials."}, status=401)
