from django.urls import path
from .views import RegisterView, LoginView, PersonalDataView, UpdateProfileView, LogoutView, ChangePasswordView, RefreshView, RequestPasswordResetView,ConfirmPasswordResetView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='token_refresh'),
    path('personal-data/', PersonalDataView.as_view(), name='personal_data'),
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('request-reset-email/', RequestPasswordResetView.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', ConfirmPasswordResetView.as_view(), name='password-reset-confirm'),
]