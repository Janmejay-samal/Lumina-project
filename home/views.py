from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product
import json


# Create your views here.
def home(request):
    # Get featured products from database (latest 3 products)
    featured_products = Product.objects.all().order_by('-created_at')[:3]
    return render(request, 'index.html', {'products': featured_products, 'is_home': True})

def products(request):
    """Main products page with filtering"""
    # Get all products from database
    products = Product.objects.all()
    
    # Get filter parameters
    category = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '')
    
    # Apply category filter
    if category != 'all':
        if category == 'limited':
            products = products.filter(is_limited=True)
        else:
            products = products.filter(category=category)
    
    # Apply search filter
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'current_category': category,
        'search_query': search_query,
    }
    return render(request, 'products.html', context)

def product_detail(request, product_id=None, slug=None):
    """Display individual product details"""
    try:
        if product_id:
            product = get_object_or_404(Product, id=product_id)
        elif slug:
            product = get_object_or_404(Product, slug=slug)
        else:
            messages.error(request, 'Product not found.')
            return redirect('products')
        
        # Get related products (same category, excluding current product)
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]
        
        context = {
            'product': product,
            'related_products': related_products,
        }
        return render(request, 'product_detail.html', context)
    except Exception as e:
        messages.error(request, f'Error loading product: {str(e)}')
        return redirect('products')

def products_by_category(request, category):
    """Filter products by category URL parameter"""
    # Validate category
    valid_categories = dict(Product.CATEGORY_CHOICES)
    
    if category == 'limited':
        products = Product.objects.filter(is_limited=True)
        category_name = 'Limited Edition'
    elif category in valid_categories:
        products = Product.objects.filter(category=category)
        category_name = valid_categories.get(category, category.title())
    else:
        messages.error(request, f'Category "{category}" not found.')
        return redirect('products')
    
    context = {
        'products': products,
        'current_category': category,
        'category_name': category_name,
    }
    return render(request, 'products.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        
        # Here you would typically send an email or save to database
        messages.success(request, f"Thank you {name}! Your message has been sent. We'll respond within 24 hours.")
        return redirect('contact')
    
    return render(request, 'contact.html', {'section': 'contact'})

@login_required(login_url='login')
def dashboard(request):
    # Get user's first name or username for display
    display_name = request.user.first_name if request.user.first_name else request.user.username
    
    # Generate user initials for avatar
    if request.user.first_name and request.user.last_name:
        user_initials = f"{request.user.first_name[0]}{request.user.last_name[0]}".upper()
    elif request.user.first_name:
        user_initials = request.user.first_name[0].upper()
    else:
        user_initials = request.user.username[0].upper()
    
    # Get real data from database (you'll need to create these models)
    # For now, keep sample data
    context = {
        'display_name': display_name,
        'user_initials': user_initials,
        'total_orders': 47,
        'wishlist_count': 23,
        'loyalty_points': '8,450',
        'recent_activities': [
            {
                'title': 'Lumina Pro Acquisition',
                'date': 'Oct 24, 2026',
                'status': 'Processing',
                'status_class': 'processing'
            },
            {
                'title': 'Nexus Subscription Renewal',
                'date': 'Oct 12, 2026',
                'status': 'Active',
                'status_class': 'active'
            },
            {
                'title': 'Lumina Air Research',
                'date': 'Saved to Wishlist',
                'status': 'Saved',
                'status_class': 'saved'
            },
            {
                'title': 'Nova Sphere Pre-order',
                'date': 'Expected Dec 2026',
                'status': 'Pre-ordered',
                'status_class': 'processing'
            },
        ]
    }
    return render(request, "dashboard.html", context)

@login_required(login_url='login')
def profile(request):
    """User profile page - View and edit profile information"""
    if request.method == 'POST':
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        # Check if username is being changed and if it's available
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                messages.error(request, 'Username already taken.')
            else:
                user.username = new_username
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'profile.html', {'user': request.user})

@login_required(login_url='login')
def order_history(request):
    """Display user's order history"""
    # Sample order data - in a real app, this would come from a database
    sample_orders = [
        {
            'id': 'LUM-1234',
            'date': 'Oct 15, 2026',
            'items': [
                {'name': 'Lumina Pro', 'quantity': 1, 'price': 1299}
            ],
            'total': 1299,
            'status': 'Delivered',
            'status_class': 'active'
        },
        {
            'id': 'LUM-5678',
            'date': 'Oct 10, 2026',
            'items': [
                {'name': 'Lumina Air', 'quantity': 2, 'price': 999}
            ],
            'total': 1998,
            'status': 'Processing',
            'status_class': 'processing'
        },
        {
            'id': 'LUM-9012',
            'date': 'Oct 5, 2026',
            'items': [
                {'name': 'Lumina Core', 'quantity': 1, 'price': 799},
                {'name': 'Lumina Mini', 'quantity': 1, 'price': 599}
            ],
            'total': 1398,
            'status': 'Shipped',
            'status_class': 'processing'
        },
    ]
    
    return render(request, 'order_history.html', {'orders': sample_orders})

def register(request):
    """Create a new user using Django's User model on POST; render the form on GET."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password')

        # Validation
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'phone': phone
            })

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'phone': phone
            })

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use another.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'phone': phone
            })

        # Password validation
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'phone': phone
            })

        try:
            # Create user
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'phone': phone
            })

    # GET -> show registration form
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return render(request, 'login.html', {'username': username})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully logged in! Welcome back, {user.first_name or username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, 'login.html', {'username': username})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return redirect('home')

# ============= NEW CART FUNCTIONALITY =============

def add_to_cart(request):
    """Shopping cart page - displays items added to cart"""
    return render(request, 'add_to_cart.html')

@login_required(login_url='login')
def cart_data(request):
    """API endpoint to get cart data for logged-in users"""
    if request.method == 'GET':
        # In a real app, you would fetch from database
        # For now, return empty cart data
        return JsonResponse({'status': 'success', 'cart': []})
    
    elif request.method == 'POST':
        # Save cart to database for logged-in user
        try:
            data = json.loads(request.body)
            cart_items = data.get('items', [])
            
            # Here you would save to database
            # For now, just return success
            return JsonResponse({'status': 'success', 'message': 'Cart saved successfully'})
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

@login_required(login_url='login')
def checkout(request):
    """Checkout page - process order"""
    if request.method == 'POST':
        # Process the order
        # Get cart data, create order, clear cart, etc.
        
        # Sample order creation
        order_id = f"LUM-{request.user.id}-{hash(request.user.username) % 10000}"
        
        messages.success(request, f'Order #{order_id} placed successfully! Thank you for your purchase.')
        return redirect('order_confirmation', order_id=order_id)
    
    return render(request, 'checkout.html')

@login_required(login_url='login')
def order_confirmation(request, order_id):
    """Order confirmation page"""
    return render(request, 'order_confirmation.html', {'order_id': order_id})

@login_required(login_url='login')
def wishlist(request):
    """User's wishlist page"""
    # Sample wishlist data
    wishlist_items = [
        {'id': 101, 'name': 'Lumina Sphere', 'price': 1499, 'in_stock': True},
        {'id': 102, 'name': 'Nova Buds Pro', 'price': 249, 'in_stock': True},
        {'id': 103, 'name': 'Celestia Watch', 'price': 599, 'in_stock': False},
    ]
    
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    # In a real app, you would save to database
    messages.success(request, f'Product added to wishlist!')
    return redirect(request.META.get('HTTP_REFERER', 'products'))

@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    # In a real app, you would remove from database
    messages.success(request, f'Product removed from wishlist!')
    return redirect('wishlist')