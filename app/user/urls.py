"""
  URLs mapping for user api.
"""
from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.CreateTokenView.as_view(), name='login'),
    path('profile/', views.ManageUserView.as_view(), name='profile')
]
