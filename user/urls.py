from django.urls import path
from .views import MyTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import VerifyEmail

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account-verify/<str:uid>/', VerifyEmail.as_view(), name='verify-email'),
]