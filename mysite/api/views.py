from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["GET"])
def hello_world(request):
    return JsonResponse({"message": "Hello, World!"})


@api_view(["POST"])
def login_view(request):
    account = request.data.get("account")
    password = request.data.get("password")

    user = authenticate(username=account, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            "message": "Login successful!",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=200)
    else:
        return JsonResponse({"message": "Invalid credentials."}, status=401)
