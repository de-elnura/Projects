from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gul/<slug:slug>/', views.category_detail, name='category_detail'),
    path('savat/', views.cart_view, name='cart_view'),
    path('savatga-qoshish/<int:flower_id>/', views.add_to_cart, name='add_to_cart'),
    path('savat-yangilash/<int:flower_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('rasmiylashtirish/', views.checkout, name='checkout'),
    path('savdolar-tarixi/', views.order_history, name='order_history'),
    path('buyurtma-bekor-qilish/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('barcha-buyurtmalarni-bekor-qilish/', views.cancel_all_orders, name='cancel_all_orders'),
    path('qayta-buyurtma/<int:order_id>/', views.reorder, name='reorder'),
    path('profil/', views.profile_view, name='profile_view'),
]
