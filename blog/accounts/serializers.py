from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.Serializer):
    first_name=serializers.CharField()
    last_name= serializers.CharField()
    email  = serializers.EmailField()
    username=serializers.CharField()
    password= serializers.CharField()

    def validate(self, data):
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('username is taken')
        
        return data
    
    def create(self, validated_data):
        user=User.objects.create(first_name=validated_data['first_name'], last_name= validated_data['last_name'], email=validated_data['email'] ,username= validated_data['username'].lower(), password=make_password(validated_data["password"]))
        return validated_data

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password= serializers.CharField()

    def validate(self, data):
        
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Account is not registered')
        
        return data
    
    def get_jwt_token(self, data):
        print(data)
        #user=User.objects.get(username=data["username"])
        user=authenticate(username=data["username"],password=data["password"])
        print(user)
        if not user:
            return{'message': 'invalid credentials','data':{}}
        refresh =RefreshToken.for_user(user)
        return {'messsage': 'Login sucessful', 'data':{'token': {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }}}
