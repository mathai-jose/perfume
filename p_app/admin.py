from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Perfume)
admin.site.register(UserDetails)
admin.site.register(admin_login)
admin.site.register(cart)
admin.site.register(CartProduct)
admin.site.register(Orders)
admin.site.register(Wishlist)