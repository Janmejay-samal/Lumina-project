from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    # Sample product data for demo
    sample_products = [
        {'id': 1, 'name': 'Lumina Pro', 'price': 1299, 'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=400&q=80'},
        {'id': 2, 'name': 'Lumina Air', 'price': 999, 'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=400&q=80'},
        {'id': 3, 'name': 'Lumina Core', 'price': 799, 'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=400&q=80'},
    ]
    return render(request, 'index.html', {'products': sample_products, 'is_home': True})

def products(request):
    # Sample product data for demo
    sample_products = [
        {'id': 1, 'name': 'Lumina Pro', 'price': 1299, 'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=400&q=80'},
        {'id': 2, 'name': 'Lumina Air', 'price': 999, 'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=400&q=80'},
        {'id': 3, 'name': 'Lumina Core', 'price': 799, 'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=400&q=80'},
    ]
    return render(request, 'products.html', {'products': sample_products})

def about(request):
    return render(request, 'about.html')

def contact(request):
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
    
    # Sample dashboard data
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