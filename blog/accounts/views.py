from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):

    def post(self, request):
        try:
            data=request.data
            serializer =RegisterSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong',
                    },status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response(
                    {
                    'data': {},
                    'message':'your account has been created',
                    },status = status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message':'something went wrong',
                    },status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
            data=request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong',
                    },status = status.HTTP_400_BAD_REQUEST)
            
            response =serializer.get_jwt_token(serializer.data)
            return Response(response,status = status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response(
                {
                'data': {},
                'message':'something went wrong'
                }, status.HTTP_400_BAD_REQUEST
            )
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request):
        try:
            print(request.data)
            refresh_token = request.data["refresh"]
            token = RefreshToken(token=refresh_token)
            token.blacklist()

            return Response({'message':'logged out successfully'},status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response({'message':'something went wrong'
                }, status.HTTP_400_BAD_REQUEST)