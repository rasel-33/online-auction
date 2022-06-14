from django.urls import path
from . import views

urlpatterns = [
    path('register-user/',views.registerUser,name='register-user'),
    path('update-profile/',views.updateProfile,name='update-profile'),
    path('signin-user/',views.signinUser,name="signin-user"),
    path('logout-user/', views.logoutUser, name="logout-user"),
    path('password_reset_request/',views.password_reset_request_view,name="password_reset_request"),
    path('reset_password/<str:token>/<str:email>/',views.changePassword,name='reset_password'),
    path('link_sent',views.linkSentView,name="link_sent"),
]
