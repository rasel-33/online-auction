from django.urls import path
from . import views

urlpatterns = [
    path('register-user/',views.registerUser,name='register-user'),
    path('update-profile/',views.updateProfile,name='update-profile'),
    path('signin-user/',views.signinUser,name="signin-user"),
    path('logout-user/', views.logoutUser, name="logout-user")
]
