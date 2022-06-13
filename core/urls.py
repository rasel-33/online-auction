from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('products',views.products,name="products"),
    path('product/<str:pk>/',views.singleproduct,name="single-product"),
    path('add-product/',views.addproduct,name="add-product"),
]