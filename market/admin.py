from django.contrib import admin
from .models import Product
from .models import Profile,Category,SubCategory

admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(SubCategory)

