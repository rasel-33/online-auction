from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('products',views.products,name="products"),
    path('product/<str:pk>/',views.singleproduct,name="single-product"),
    path('add-product/',views.addproduct,name="add-product"),
    path('auction_products/',views.live_auction_products,name="auction_products"),
    path('auction_single_product/<str:pk>/',views.single_auction_product,name="auction_single_product"),
    path('product_update/<str:pk>/',views.update_product,name="product_update"),
    path('delete_product/<str:pk>/',views.delete_product,name="delete_product"),
    path('no_permission',views.no_permission,name="no_permission"),
    path('my_prouducts',views.my_products,name="my_products"),
    path('place_bid/<str:pk>/',views.PlaceBidForm,name="place_bid"),
    path('auction_history/<int:pk>', views.auction_history, name="auction_history"),
]