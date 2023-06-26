from django.urls import path
from catalog.views import index, contacts, product_card

urlpatterns = [
    path('', index),
    path('contacts/', contacts, name='contacts'),
    path('product_card/<int:pk>/', product_card, name='product_card')
]
