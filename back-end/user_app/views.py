from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as s
from django.contrib.auth import authenticate, login, logout


# Create your views here.
class Register(APIView):
    def post(self, request):
        data = request.data.copy()
        new_user = UserSerializer(data=data, partial=True)
        if new_user.is_valid():
            user = new_user.save()
            token = Token.objects.create(user=user)
            login(request, user)
            return Response(
                {"user": user.username, "token": token.key}, status=s.HTTP_201_CREATED
            )
        else:
            return Response(new_user.errors, status=s.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    def post(self, request):
        data = request.data.copy()
        user = authenticate(username=data.get("email"), password=data.get("password"))
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"user": user.username, "token": token.key}, status=s.HTTP_200_OK
            )
        else:
            return Response("No User Matching Credentials", status=s.HTTP_404_NOT_FOUND)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class LogOut(UserView):
    def post(self, request):
        user = request.user
        user.auth_token.delete()
        logout(request)
        return Response("You have successfully logged out", status=s.HTTP_200_OK)

class UserInfo(UserView):
    def get(self, request):
        user = UserSerializer(request.user)
        return Response(user.data)
    
    def put(self, request):
        user = UserSerializer(request.user, data=request.data, partial=True)
        if user.is_valid():
            user.save()
            return Response(user.data)
        else:
            return Response(user.errors, status=s.HTTP_400_BAD_REQUEST)