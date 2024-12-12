from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from .serializers import RegisterResponseSerializer, RegisterSerializer, PersonalDateViewSerializer, PasswordResetConfirmSerializer, RequestPasswordResetViewSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication"],
        summary="Register new user",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(
                description="User created successfully",
                response=RegisterResponseSerializer,
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "message": "User created successfully",
                            "username": "user123",
                            "email": "example@example.com",
                            "date_joined": "2021-07-16T15:00:00"
                        }
                    )
                ]
            ),
        },
    )
    def post(self, request):
        input_serializer = RegisterSerializer(data=request.data)
        
        if input_serializer.is_valid():
            user = User.objects.create_user(
                username=input_serializer.validated_data["username"],
                password=input_serializer.validated_data["password"],
                email=input_serializer.validated_data["email"]
            )
            output_serializer = RegisterResponseSerializer({
                "message": "User created successfully",
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined
            })
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    @extend_schema(
        tags=["Authentication"],
        summary="Login user"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

#post method is already implemented in TokenObtainPairView

class RefreshView(TokenRefreshView):
    
    @extend_schema(
        tags=["Authentication"],
        summary="Refresh token"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PersonalDataView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Authentication"],
        summary="Get personal data of the authenticated user",
        responses={
            200: OpenApiResponse(
                description="Data of the authenticated user",
                response=PersonalDateViewSerializer,
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "username": "user123",
                            "email": "example@example.com",
                            "date_joined": "2021-07-16T15:00:00",
                            "is_superuser": False,
                            "user_permissions": ["view_user", "add_user"],
                            "first_name": "John",
                            "last_name": "Doe"
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request):
        # Obtener al usuario autenticado
        user = request.user

        # Preparar los datos del usuario
        user_data = PersonalDateViewSerializer({
            "username": user.username,
            "email": user.email,
            "date_joined": user.date_joined,
            "is_superuser": user.is_superuser,
            "user_permissions": list(user.get_all_permissions()),
            "first_name": user.first_name if user.first_name else None,
            "last_name": user.last_name if user.last_name else None
        }).data

        return Response(user_data, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        tags=["Authentication"],
        summary="Update profile of the authenticated user"
    )

    def put(self, request):
        user = request.user
        firstName = request.data.get('firstName')
        lastName = request.data.get('lastName')
        email = request.data.get('email')

        if email:
            user.email = email
        if firstName:
            user.first_name = firstName
        if lastName:
            user.last_name = lastName

        user.save()
        return Response(PersonalDateViewSerializer({
            "username": user.username,
            "email": user.email,
            "date_joined": user.date_joined,
            "is_superuser": user.is_superuser,
            "user_permissions": list(user.get_all_permissions()),
            "first_name": user.first_name if user.first_name else None,
            "last_name": user.last_name if user.last_name else None
        }).data, status=status.HTTP_200_OK)
        
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        tags=["Authentication"],
        summary="Change password"
    )

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirmation = request.data.get('new_password_confirmation')
        
        if not old_password or not new_password or not new_password_confirmation:
            if new_password != new_password_confirmation:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'})
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        tags=["Authentication"],
        summary="Logout user"
    )

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        

## Reset Password
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        tags=["Authentication"],
        summary="Request password reset",
        request=RequestPasswordResetViewSerializer,
        responses={
            200: OpenApiResponse(
                description="Password reset token sent to email",
                
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "Reset link sent to email": "http://localhost:8000/password_reset/uid/token/"
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Email not found",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={
                            "error": "Email not found"
                        }
                    )
                ]
            ),
        },
    )

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            reset_token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_link = f'http://localhost:8000/password_reset/{uid}/{reset_token}/'
            
            """ send_mail(
                'Password Reset',
                f'Use this link to reset your password: {reset_link}',
                'from@example.com',
                [email],
                fail_silently=False,
            ) """
            return Response({'message': 'Password reset link sent to email', 'reset_link': reset_link})
        except User.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
        
class ConfirmPasswordResetView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        tags=["Authentication"],
        summary="Confirm password reset",
        request=PasswordResetConfirmSerializer,
        responses={
            200: OpenApiResponse(
                description="Password reset confirmed successfully",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={"message": "Password reset confirmed successfully"}
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        "Response Example",
                        value={"error": "Invalid token or uid"}
                    )
                ]
            )
        }
    )
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = PasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"message": "Password reset confirmed successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid token or uid"}, status=status.HTTP_400_BAD_REQUEST)
