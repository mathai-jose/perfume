from django.shortcuts import render,redirect
from django.db import transaction
from .models import *
from django.db.models import Q
from django.contrib import messages
from . forms import checkoutform
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  Perfume
def admin_view(request):
    p = Perfume.objects.all()
    context = {'P':p}
    return render(request,'admin_view.html',context)

def admin_perfume_add(request):
    if request.method == "POST":
        name = request.POST['pname']
        desc = request.POST['pdesc']
        frag = request.POST['pfragrance']
        price = request.POST['pprice']
        quantity = request.POST['pquantity']
        image = request.FILES['pimage']
        # Check if the price is valid
        if not price.isdigit() or int(price) <= 0:
            messages.error(request, "Please enter a valid price greater than 0.")
            return redirect('admin_perfumeadd')
        if Perfume.objects.filter(p_name=name).exists():
                messages.info(request,"Perfume with this name already exists.")
                return redirect('admin_perfumeadd')
        perfumes = Perfume.objects.create(p_name = name,p_desc = desc,p_fragrance=frag,p_quantity = quantity,p_price = price,p_image = image)
        perfumes.save()
        messages.success(request, "Product Added Successfully!")
        return redirect('admin_view')
    return render(request,'admin_perfumeadd.html')
from decimal import Decimal
def admin_perfume_update(request,pk):
    p = Perfume.objects.get(pk=pk)
    
    if request.method == 'POST':
        if 'pname' in request.POST:
            p.p_name = request.POST['pname']
        if 'pdesc' in request.POST:
            p.p_desc = request.POST['pdesc']
        if 'pfragrance' in request.POST:
            p.p_fragrance = request.POST['pfragrance']
        if 'pprice' in request.POST:
            price = request.POST['pprice']
            try:
                price = Decimal(price)
                if price <= 0:
                    messages.error(request, "Please enter a valid price greater than 0.")
                    return redirect('admin_perfumeupdate', pk=pk)
                p.p_price = price
            except ValueError:
                messages.error(request, "Please enter a valid numeric price.")
                return redirect('admin_perfumeupdate', pk=pk)
        if 'pquantity' in request.POST:
            p.p_quantity = request.POST['pquantity']
        if 'pimage' in request.FILES:
            p.p_image = request.FILES['pimage']
        
        p.save()

        messages.success(request, "Product Updated Successfully!")
        return redirect('admin_view')
    
    context = {'P': p}
    return render(request,'admin_perfumupdate.html',context)

def admin_perfume_delete(request,pk):
    try:
        p = Perfume.objects.filter(pk=pk)
        p.delete()
        messages.success(request,"Product Deleted Successfully!")
        return redirect('admin_view')
        # return HttpResponse("<h1 style='color:Black;text-align:center;margin-top:20%;'>Product Deleted Successfully</h1>")
    except Perfume.DoesNotExist:
        messages.error(request,'Product Not Found')
        return redirect('admin_view')

from django.contrib import messages

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile_phone = request.POST.get('phone')

        # Check if the username already exists
        if UserDetails.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return render(request, 'register.html')

        if first_name and last_name and username and password and mobile_phone:
            user = UserDetails.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                mobile_phone=mobile_phone
            )
            user.save()
            return redirect('login')
    
    return render(request, 'register.html')

     
def userLogin(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=UserDetails.objects.filter(username=username,password=password)
        admin=admin_login.objects.filter(username=username,password=password)

        if len(user) >= 1:
            request.session['user_id']=user[0].id
            return redirect('homepage')
        elif len(admin) >= 1:
            request.session['user_id']=admin[0].id
            return redirect('admin_view')

        else:
            messages.info(request,'Invalid Username or Password')
            return redirect('login')
    else:
        return render(request,'login.html')
    
def home_page(request):
    p = Perfume.objects.all()[:3]
    context = {'P':p}
    return render(request,'home.html',context)

def user_logout(request):
    del request.session['user_id']
    return redirect('homepage')

def allProducts(request):
    p = Perfume.objects.all()
    context = {'P':p}
    return render(request,'shop.html',context)

def view_product(request,id):
    product=Perfume.objects.get(p_id=id)
    return render(request,'product_detail.html',{'perfume':product})

def mycart(request):
    user_id = request.session['user_id']
    up = UserDetails.objects.get(id=int(user_id))
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart1 = cart.objects.get(id=cart_id)
    else:
        cart1 = None
    context = {'cart': cart1,'u':up}


    return render(request, 'mycart.html', context)

def addtocart(request, id):
    try:
        product_obj = Perfume.objects.get(p_id=id)
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_obj = cart.objects.get(id=cart_id)
            product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            # item already exist in cart
            if product_in_cart.exists():
                cartproduct = product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.p_price
                cartproduct.save()
                cart_obj.total += product_obj.p_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.p_price,
                                                        quantity=1, subtotal=product_obj.p_price)
                cart_obj.total += product_obj.p_price
                cart_obj.save()
        else:
                user_id = request.session['user_id']
                up = UserDetails.objects.get(id=int(user_id))
                cart_obj = cart.objects.create(customer=up,total=0)
                request.session['cart_id'] = cart_obj.id
                print("new cart")
                cp = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.p_price, quantity=1,
                                                        subtotal=product_obj.p_price)
                cart_obj.total += product_obj.p_price
                cart_obj.save()
    except:
        messages.error(request, "Login to add to Cart!")
    return redirect("/")

def managecart(request, id):
    print("im in manage cart")
    action = request.GET.get("action")
    cp_obj = CartProduct.objects.get(id=id)
    cart_obj = cp_obj.cart

    if action == "inc":
        cp_obj.quantity += 1
        cp_obj.subtotal += cp_obj.rate
        cp_obj.save()
        cart_obj.total += cp_obj.rate
        cart_obj.save()
    elif action == "dcr":
        cp_obj.quantity -= 1
        cp_obj.subtotal -= cp_obj.rate
        cp_obj.save()
        cart_obj.total -= cp_obj.rate
        cart_obj.save()
        if cp_obj.quantity == 0:
            cp_obj.delete()
            del request.session['cart_id']
    elif action == 'rmv':
        cart_obj.total -= cp_obj.subtotal
        cart_obj.save()
        cp_obj.delete()
    else:
        pass
    return redirect('/my-cart')

def emptycart(request):
    cart_id=request.session.get("cart_id",None)
    cart1=cart.objects.get(id=cart_id)
    cart1.cartproduct_set.all().delete()
    cart1.total=0
    cart1.save()

    return redirect('/my-cart')

def checkout(request):
    user_id=request.session['user_id']
    user=UserDetails.objects.get(id=user_id)
    cart_id = request.session.get("cart_id")
    cart_obj = cart.objects.get(id=cart_id)
    form = checkoutform(request.POST)
    if request.method == "POST":
        order_status = "Order recived"
        address = request.POST["address"]
        mobile =request.POST["contact"]
        total = request.POST["total"]
        with transaction.atomic():
            cart_products = CartProduct.objects.filter(cart=cart_obj)
            for cart_product in cart_products:
                product = cart_product.product
                product.p_quantity -= cart_product.quantity
                product.save()
        new_order = Orders.objects.create(cart=cart_obj, customer=user, address=address, mobile=mobile,
                                              total=total, order_status=order_status)
        new_order.save()
        del request.session['cart_id']
        messages.info(request,"Order Placed")
        return redirect('/')
    else:
        context = {'cart': cart_obj, 'form': form,'user': user}
        return render(request, 'checkout.html', context)

def my_orders(request):
    user_id = request.session['user_id']
    up = UserDetails.objects.get(id=int(user_id))
    
    user_orders = Orders.objects.filter(customer=up).order_by('-created_at')

    return render(request, 'my_orders.html', {'user_orders': user_orders})

def searchresult(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Perfume.objects.all().filter(Q(p_name__contains=query) | Q(p_desc__contains=query) | Q(p_fragrance__contains=query) | Q(p_desc__contains=query))
        return render(request, 'search.html', {'query': query, 'products': products})
    
@login_required
def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Perfume, p_id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        return redirect('wishlist')
    else:
        # Handle the case where the request method is not POST (optional)
        return render(request, 'shop.html')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Perfume, p_id=product_id)  # Assuming 'p_id' is the primary key of Perfume model
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')