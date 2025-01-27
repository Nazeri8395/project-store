
from django.urls import path
from .views import RegisterView, LoginView, MobileNumberCheckView

urlpatterns = [
        path('register/',RegisterView.as_view(), name='register'),
        path('login/', LoginView.as_view(), name='login'),
        path('api/check-mobile/', MobileNumberCheckView.as_view(), name='check-mobile'),
]
