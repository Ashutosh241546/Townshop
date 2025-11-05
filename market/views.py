from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from mamatajwells.models import Jewellery
from market.models import Product,Profile,CartItem,Order,OrderItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import ProfileForm
from decimal import Decimal

def protected_view(view_func):
    """
    Ye decorator ensure karta hai ki sirf logged-in user hi view access kare.
    Logout ke baad back button se bhi access blocked.
    """
    @never_cache
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper


def home(request):
    jewellery_products = Jewellery.objects.all()
    market_products = Product.objects.all()
    return render(request, 'home.html', {
        'jewellery_products': jewellery_products,
        'market_products': market_products,
    })

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # next parameter handle karo
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # <-- yahan 'login' karo instead of 'home'

@protected_view
def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

@login_required(login_url='/login/')
def about_view(request):
    return render(request, 'about.html')
@login_required
def contact_view(request):
    return render(request, 'contact.html')



@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        # 👇 yahan hum initial data set kar rahe hain
        form = ProfileForm(instance=profile, initial={
            'full_name': profile.full_name or request.user.get_full_name(),
        })

    return render(request, 'profile.html', {'form': form})


# def profile_view(request):
#     return render(request, 'profile.html')
@login_required
def add_to_cart(request, product_id, product_type):
    if product_type == 'market':
        product = get_object_or_404(Product, id=product_id)
    else:
        product = get_object_or_404(Jewellery, id=product_id)

    # Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product_id=product.id,  # ✅ yahan product ki real id save karo
        product_type=product_type,
        defaults={
            'product_name': product.name,
            'price': product.price,
            'quantity': 1
        }
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')



@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

# ✅ Update quantity (+ / -)
@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    action = request.POST.get('action')  # 'increase' ya 'decrease'

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # agar quantity 1 hai aur decrease, to remove item

    return redirect('cart_view')


# ✅ Remove item completely
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def checkout_view(request):
    # yahan checkout logic ya summary add kar sakte ho
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.price * item.quantity for item in items)
    return render(request, 'checkout.html', {'items': items, 'total': total})

@login_required
def product_detail(request, pk):
    # Get the current product
    product = get_object_or_404(Product, pk=pk)
    
    # Get other products to show in "You may also like"
    related_products = Product.objects.exclude(pk=pk)[:4]  # optional limit

    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })


@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.price * item.quantity for item in cart_items)
    
    # Fixed village delivery charges
    villages = {
        "Sawayajpur": 50,
        "Bhukhnahi": 60,
        "Semarua": 40,
        "Kundauli": 55,
        "Tirma": 70,
        "Manjhawan": 65,
        "Khujhauli": 45,
        "Chirli": 50,
        "Roshanpur": 60,
        "Tikariya": 55,
        "Pali": 50
    }

    if request.method == 'POST':
        village = request.POST.get('village')
        landmark = request.POST.get('landmark')
        payment_method = request.POST.get('payment_method', 'cod')

        delivery_charge = villages.get(village, 0)

        # Convert Decimal to float for session
        request.session['checkout'] = {
            'subtotal': float(subtotal),
            'delivery_charge': float(delivery_charge),
            'total': float(subtotal + delivery_charge),
            'village': village,
            'landmark': landmark,
            'payment_method': payment_method
        }

        return redirect('checkout_success')  # success page URL name

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'villages': villages
    })

@login_required
def checkout_success(request):
    checkout_data = request.session.get('checkout')
    if not checkout_data:
        return redirect('cart_view')

    # ✅ Clear the cart for this user
    CartItem.objects.filter(user=request.user).delete()

    # Optionally, save order to DB here
    return render(request, 'checkout_success.html', {
        'checkout': checkout_data
    })








