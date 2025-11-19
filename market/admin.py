# from django.contrib import admin
# from .models import Product
# from .models import Profile,Category,SubCategory

# admin.site.register(Product)
# admin.site.register(Profile)
# admin.site.register(Category)
# admin.site.register(SubCategory)
from django.contrib import admin
from .models import Category, SubCategory, Product, Profile, CartItem, Order, OrderItem

# -------------------------
# CATEGORY ADMIN
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name",)


# -------------------------
# SUBCATEGORY ADMIN
# -------------------------
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category__type", "category")
    search_fields = ("name",)


# -------------------------
# PRODUCT ADMIN
# -------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product_type", "category", "subcategory", "price", "vendor_id")
    list_filter = ("product_type", "category", "subcategory")
    search_fields = ("name", "description")
    list_editable = ("price",)

    # Vendor ko sirf apne product dekhne ka option future me laga sakte ho
    # but abhi full admin ko dikhega.


# -------------------------
# PROFILE ADMIN
# -------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone", "city", "is_vendor")
    list_filter = ("is_vendor", "city")
    search_fields = ("user__username", "full_name")
    list_editable = ("is_vendor",)


# -------------------------
# ORDER ITEM INLINE
# -------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "product_type", "price", "quantity")


# -------------------------
# ORDER ADMIN
# -------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "village", "total_price", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "village")
    inlines = [OrderItemInline]


# -------------------------
# ORDER ITEM ADMIN
# -------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "product_type", "price", "quantity")
    search_fields = ("product_name",)
    list_filter = ("product_type",)


# -------------------------
# CART ITEM ADMIN
# -------------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product_name", "product_type", "price", "quantity")
    search_fields = ("user__username", "product_name")
    list_filter = ("product_type",)



