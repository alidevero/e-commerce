from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email']


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email','first_name','last_name','password']
        extra_kwargs = {'password':{'write_only':True}}

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required")
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("Account with same email exists")
        return value
        
    def validate_password(self, value):
        if len(value)< 8:
            raise serializers.ValidationError("Password must be 8 characters")
        if not any(  char.isdigit() for char in value):
            raise serializers.ValidationError("Password must have characters")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Passsword must have numbers")
        return value
    
class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    email = serializers.EmailField()

    def validate_OTP(sefl,value):
        if not value:
            raise serializers.ValidationError("OTP is reuired")
        return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email= email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")
        return data
    

class PatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name']



        