
#System Imports
import random
from tokenize import TokenError

#project imports
from django.shortcuts import render
from rest_framework.views import APIView , Response
from django.core.cache import cache
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.permissions import IsAuthenticated

#Local Imports
from .serializers import *
from .utils import *
# Create your views here.


class SignupView(APIView):
    
    def post(self , request):
        try:
            data = request.data
            serializer = SignUpSerializer(data = data)
            if serializer.is_valid():
                otp = random.randint(1000,9999)
                email = serializer.validated_data.get("email")

                payload = {
                    **serializer.validated_data,
                    "otp":otp
                }
                cache_key = f"email_otp{email}"
                cache.set(cache_key,payload,timeout=600)

                email_sent = send_otp_via_mail(email , otp)
                print(f"This email have sent{email_sent}")
                if not email_sent:
                    return Response({
                        "detail":"Failed to send OTP"
                    },status= status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response({
                    "detail":"OTP send successfully please check you email"
                },status= status.HTTP_200_OK)
            return Response({"response":serializer.errors},status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "detail":str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class VerifyOTP(APIView):
    def post(slef , request):
        try:
            data = request.data
            serializer = OTPVerifySerializer(data=data)
            if serializer.is_valid():
                otp_submited_by_user = serializer.validated_data.get("otp")
                email = serializer.validated_data.get("email")
                cache_key = f"email_otp{email}"
                payload = cache.get(cache_key)
                if not payload:
                    return Response({"detail":"OTP expired or not found"})
                otp_sent_by_us = payload["otp"]
                if otp_submited_by_user != otp_sent_by_us:
                    return Response({"detail":"Invalid OTP or expired"},status=status.HTTP_400_BAD_REQUEST)
                try:
                    user = User.objects.create(
                        first_name = payload["first_name"],
                        last_name = payload["last_name"],
                        email = payload["email"],
                        password = make_password(payload["password"])
                    )
                except Exception as e:
                    return Response({"detail":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                user.save()
                cache.delete(cache_key)
                return Response({"detail":"Accoount created successfully"},status=status.HTTP_200_OK)
            return Response({"detail":"Validation failed"},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "detail":str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class LoginView(APIView):
    
    def post(self , requst):
        try:
            data = requst.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                user = User.objects.get(email = serializer.validated_data['email'])
                refresh = RefreshToken.for_user(user)
                return Response({"detail":"LogedIn successfully","refresh":str(refresh),"access":str(refresh.access_token)},status=status.HTTP_200_OK)
            return Response({"detail":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self , request):
        try:
            user = request.user
            user.delete()
            return Response({"detail":"Account deleted Successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self , request):
        try:
            data = request.data
            user = request.user
            serializer = PatchSerializer(instance = user ,data= data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail":"User updated Successfully"},status=status.HTTP_200_OK)
            return Response({"detail":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail":str(e)},status=status.HTTP_400_BAD_REQUEST)
            

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request):
        try:
            serializer = UserSerializer(request.user)
            
            return Response({"detail":"Successfully got user","data":serializer.data})
            
        except Exception as e:
            return Response({"detail":str(e)},status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        