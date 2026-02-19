from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Main Pages
    path('', views.home, name='home'),
    path('home/', views.home, name='home_alt'),
    path('products/', views.products, name='products'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.order_history, name='order_history'),
    
    # Product Details (NEW - for individual product pages)
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail_slug'),
    
    # Cart URLs
    path('cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/data/', views.cart_data, name='cart_data'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # Wishlist URLs
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Category Filtering (NEW)
    path('products/category/<str:category>/', views.products_by_category, name='products_by_category'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)