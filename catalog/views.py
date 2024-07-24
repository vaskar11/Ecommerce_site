from django.shortcuts import render,redirect
from django.http import HttpResponse
from catalog.models import Category,Product, ShoppingCart,ShoppingOrder,DeliveryAddress
from catalog.forms import ProductForm,CategoryForm,SignupForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    products= Product.objects.all()
    return render(request, 'index.html',{'products':products})

def user_signup(request):
    if request.method=="POST":
        print(request.POST)
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form=SignupForm()
    return render(request, "signup.html",{'form':form})

def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect("/")
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})


def user_logout(request):
    print("hello")
    logout(request)
    return redirect('/login/')

def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/create/product')
    else:
        form = ProductForm()
    context_dir = {
        'form':form 
    }
    return render(request, "create_product.html", context_dir)

def list_product(request):
    products = Product.objects.all()
    context_dir ={
        'products':products
    } 
    return render(request,"list_product.html",context_dir )


def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/create/category')
    else:
        form = CategoryForm()
    context_dir = {
        'form':form 
    }
    return render(request, "create_category.html", context_dir)


def list_category(request):
    products = Category.objects.all()
    context_dir ={
        'products':products
    } 
    return render(request,"list_category.html",context_dir )

def update_product(request,id):
    product=Product.objects.get(id=id)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('/list/product')
    else:
        form = ProductForm(instance= product)
    return render(request, "create_product.html", {'form': form})



def delete_product(request,id):
    product= Product.objects.get(id=id)
    product.delete()
    return redirect('/list/product')
 
 #for shopping cart

def product_detail(request, id):
     product = Product.objects.get(id=id)
     return render(request, "product_detail.html",{'product':product})
 
@login_required(login_url="/login/")
def add_to_cart(request, id):
    product= Product.objects.get(id=id)
    quantity = request.POST['quantity']
    user= User.objects.get(id= request.user.id)
    cart = ShoppingCart(product= product, user= user, quantity= quantity)
    cart.save()
    return HttpResponse("Succes <a href ='/'> GO back </a>")


@login_required(login_url="/login/")
def cart_detail(request):
    user= User.objects.get(id= request.user.id)
    items= ShoppingCart.objects.filter(user=user)
    return render(request,'cart_detail.html',{'items':items})
    
@login_required(login_url="/login/")
def cart_item_delete(request,id):
    cart= ShoppingCart.objects.get(id=id)
    cart.delete()
    return redirect("/my/cart/")
    
@login_required(login_url="/login/")     
def cart_item_update(request, id):
    cart= ShoppingCart.objects.get(id=id)
    if request.method =="POST":
        print(request.POST)
        quantity=  request.POST['quantity']
        cart.quantity = quantity
        cart.save()
        return redirect('/my/cart/')
    return render(request,"cart_item_update.html",{'cart':cart})
   
@login_required(login_url="/login/")
def order_checkout(request):
    user = User.objects.get(id=request.user.id)
    items = ShoppingCart.objects.filter(user=user)
    total_amount = 0
    for item in items:
        total_amount = total_amount+((item.quantity)*(item.product.price))
    shop_order = ShoppingOrder(user=user,total_amount=total_amount)
    shop_order.save()
    return redirect(f'/payment/{shop_order.id}/')
    
@login_required(login_url="/login/")
def make_payment(request,id):
    shop_order = ShoppingOrder.objects.get(id=id)
    if request.method=='POST':
        paid_amount = request.POST['paid_amount']
        payment_mode = request.POST['payment_mode']
        shop_order.paid_amount = paid_amount
        shop_order.payment_mode = payment_mode
        shop_order.save() 
        return redirect(f'/delivery/address/{shop_order.id}/')
    return render(request,'payment.html',{'shop_order':shop_order})


@login_required(login_url="/login/")
def order_delivery_address(request,id):
    shop_order = ShoppingOrder.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    delivery_address = DeliveryAddress.objects.filter(user = user)
    if request.method=='POST':
        delivery_address = DeliveryAddress.objects.create(user=user,address = request.POST['address'])
        shop_order.address = delivery_address
        shop_order.payment_status = '0'
        shop_order.delivery_status = '0'
        shop_order.save()
        return HttpResponse('<h1>Order Placed Successfully</h1>.<a href="/">Home</a>')
    return render(request,'address.html',{'shop_order':shop_order,'delivery_address':delivery_address})


@login_required(login_url="/login/")
def place_order(request,id):
    user = User.objects.get(id=request.user.id)
    delivery_address = DeliveryAddress.objects.filter(user = user)[0]
    shop_order = ShoppingOrder.objects.get(id=id)
    shop_order.address = delivery_address.address
    shop_order.payment_status = '0'
    shop_order.delivery_status = '0'
    shop_order.save()
    return HttpResponse('<h1>Order Placed Successfully</h1>.<a href="/">Home</a>')



