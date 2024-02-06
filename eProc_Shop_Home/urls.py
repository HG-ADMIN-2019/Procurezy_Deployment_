from django.urls import path

from . import views


app_name = 'eProc_Shop_Home'

urlpatterns = [
    path('', views.shopping_cart_home, name='shopping_cart_home'),
    path('add_favourite_shopping_cart/', views.add_favourite_shopping_cart, name='add_favourite_shopping_cart'),
    path('delete_recently_viewed_item/', views.delete_recently_viewed_item, name='delete_recently_viewed_item'),
    path('add_fav_sc_to_cart/', views.add_fav_sc_to_cart, name='add_fav_sc_to_cart'),
    path('delete_favourite_shopping_cart/', views.delete_favourite_shopping_cart, name='delete_favourite_shopping_cart'),
]