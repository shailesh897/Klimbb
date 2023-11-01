from django.urls import path
from .views import LoginView, ActivateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('activate/', ActivateView.as_view(), name='activate'),
]
