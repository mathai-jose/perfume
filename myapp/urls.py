from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index,name='index'),
    path('admin_perfumeadd',views.admin_perfume_add,name='admin_perfumedd'),
    path('admin_perfumeupdate',views.admin_perfume_update,name='admin_perfumeupdate'),
 
]
