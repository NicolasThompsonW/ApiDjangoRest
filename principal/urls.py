from .views import ProtectedView, PersonalDataView
from django.urls import path

urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('personal-data/', PersonalDataView.as_view(), name='personal_data'),
]