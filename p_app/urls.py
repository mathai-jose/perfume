from django.urls import path
from . import views
from .views import *
urlpatterns = [

    path('admin_view',views.admin_view,name='admin_view'),
    path('admin_perfumeadd',views.admin_perfume_add,name='admin_perfumeadd'),
    path('admin_perfumeupdate/<int:pk>/',views.admin_perfume_update,name='admin_perfumeupdate'),
    path('admin_perfumedelete/<int:pk>/',views.admin_perfume_delete,name='admin_perfumedelete'),
    path('register',register,name='register'),
    path('login',userLogin,name='login'),
    path('',home_page,name='homepage'),
    path('logout/', user_logout, name='logout'),
    path('allproducts',allProducts,name='allProducts'),
    path('view-product/<int:id>',view_product),
    path('add-to-cart/<int:id>',views.addtocart),

    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist,name='remove_from_wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('search/', views.searchresult, name='search'),

    path('my-cart',views.mycart, name='my-cart'),

    path('managecart/<int:id>/',views.managecart,name="managecart"),

    path("empty-cart/",views.emptycart),

    path("checkout",views.checkout),
    path('my-orders',my_orders,name='my-orders')

 
]
