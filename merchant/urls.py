from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.merchant_dashboard, name='merchant_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
]
