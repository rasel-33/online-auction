from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('products',views.products,name="products"),
    path('product/<str:pk>/',views.singleproduct,name="single-product"),
    path('add-product/',views.addproduct,name="add-product"),
    path('auction_products/',views.live_auction_products,name="auction_products"),
    path('auction_single_product/<str:pk>/',views.single_auction_product,name="auction_single_product"),
]