from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    pass

#post method is already implemented in TokenObtainPairView
class RefreshView(TokenRefreshView):
    pass

class PersonalDataView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request):
        # Obtener al usuario autenticado
        user = request.user

        # Preparar los datos del usuario
        user_data = {
            "username": user.username,
            "email": user.email,
            "date_joined": user.date_joined,
            "is_superuser": user.is_superuser,
            "user_permissions": list(user.get_all_permissions()),
            "first_name": user.first_name if user.first_name else None,
            "last_name": user.last_name if user.last_name else None
        }

        return Response(user_data)
    

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

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
        return Response({'message': 'Profile updated successfully'})
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

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

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            reset_token = get_random_string(32)  # Genera un token aleatorio
            user.profile.reset_token = reset_token
            user.profile.save()

            # Envía un email con el token
            send_mail(
                'Password Reset',
                f'Use this token to reset your password: {reset_token}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset token sent to email'})
        except User.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
        
class ConfirmPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        new_password_confirmation = request.data.get('new_password_confirmation')
        
        if not token or not new_password or not new_password_confirmation:
            if new_password != new_password_confirmation:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(profile__reset_token=token)
            user.set_password(new_password)
            user.profile.reset_token = None
            user.profile.save()
            return Response({'message': 'Password reset successfully'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
