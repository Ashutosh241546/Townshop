from django.urls import path
from mamatajwells.views import *

app_name = 'mamatajwells'

urlpatterns = [
    path('welcome/', jwells_home, name='jwells_home'),
    path('collection/', jewellery_list, name='list'),
    path('detail/<int:pk>/', jewellery_detail, name='detail'),
]
