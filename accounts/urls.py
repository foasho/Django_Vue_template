from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
