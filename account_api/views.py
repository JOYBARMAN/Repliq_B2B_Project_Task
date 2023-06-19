from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserRegistrationSerializer , UserLoginSerializer ,UserProfileSerializer, UserChangePasswordSerializer ,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from account_api.models import User


# generate token munually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# user registration view 
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderers]
    @extend_schema(
    request=UserRegistrationSerializer,
    responses={201: UserRegistrationSerializer},
    )
    def post(self,request,format=None):
        '''User registration view'''
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({"token":token,"account_type":"merchant account","msg":"Registration Sucessful"},status=status.HTTP_201_CREATED)

# user login view 
class UserLoginView(APIView):
    renderer_classes = [UserRenderers]
    @extend_schema(
    request=UserLoginSerializer,
    responses={201: UserLoginSerializer},
    )
    def post(self,request,format=None):
        '''User login view'''
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.data.get("email")
        password=serializer.data.get("password")
        user=authenticate(email=email,password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"token":token,"msg":"Login Sucessful"},status=status.HTTP_200_OK)
        else:
            return Response({"errors":{"non_field_errors":"Email or Password is not valid"}},status=status.HTTP_404_NOT_FOUND)  
            
# user profile view 
class UserProfileView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        '''User profile view'''
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# user change password
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    @extend_schema(
    request=UserChangePasswordSerializer,
    responses={201: UserChangePasswordSerializer},
    )

    def post(self,request,format=None):
        '''After login user can change his password'''
        serializer = UserChangePasswordSerializer(data=request.data,context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"msg":"Password Sucessfully Changed"},status=status.HTTP_200_OK)

# views for send email for reseting password
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderers]
    @extend_schema(
    request=SendPasswordResetEmailSerializer,
    responses={201: SendPasswordResetEmailSerializer},
    )
    def post(self,request,format=None):
        '''User can send mail for password reset (forgot password)'''
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"msg":"Password Reset link send , Please check your email"},status=status.HTTP_200_OK)


# views for user password reset 
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderers]
    @extend_schema(
    request=UserPasswordResetSerializer,
    responses={201: UserPasswordResetSerializer},
    )
    def post(self,request,uid,token,format=None):
        '''User can reset his password through link provide in mail'''
        serializer=UserPasswordResetSerializer(data=request.data,context={"user_id":uid,"token":token})
        serializer.is_valid(raise_exception=True)
        return Response({"msg":"Password Sucessfully Changed"},status=status.HTTP_200_OK)
    

class UserList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        """Get all user of the system"""
        all_user = User.objects.all()
        serializer = UserProfileSerializer(all_user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)