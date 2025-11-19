from django.urls import path
from market.views import *


urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('products/', product_list, name='products'), 
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('profile/', profile_view, name='profile'),
    path('add-to-cart/<int:product_id>/<str:product_type>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/update/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/success/', checkout_success, name='checkout_success'),
    path('order-history/', order_history, name='order_history'),
    path('order_detail/', order_detail, name='order_detail'),
    path('place_order/', place_order, name='place_order'),
    path('daily-deals/', daily_deals, name='daily_deals'),
    path("dashboard/", vendor_dashboard, name="vendor_dashboard"),
    path("add-product/", vendor_add_product, name="vendor_add_product"),
    path('vendor/setup/', vendor_shop_setup, name='vendor_shop_setup'),
    path('vendor/vendor_list', vendor_list, name='vendor_list'),
    path("vendor/products/<int:vendor_id>/", vendor_product_list, name="vendor_product_list"),




]


