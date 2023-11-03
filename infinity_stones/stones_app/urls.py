from django.urls import path
from .views import LoginView, ActivateView, StoneStatusView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('activate/', ActivateView.as_view(), name='activate'),
    path('status/<int:User_ID>/', StoneStatusView.as_view(), name='user-activation-status'),
]
