from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import *
from .forms import *
from django.contrib import messages
import json
from django.core.paginator import Paginator

from urllib.request import Request, urlopen
import bs4, requests





def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)

                    messages.success(request, f'Your account has been created!')
                    return redirect('core:home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})



@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def home(request):
    return render(request, 'core/home.html')


@login_required
def traveller(request):

    if hasattr(request.user, 'travellerUser'):
        products=ProductBuyer.objects.filter(traveller=request.user.travellerUser);

        context = {
        'products': products,

        }

        return render(request, 'core/tchoose.html', context)


    else:

        template_name = 'core/traveller.html'

        if request.method == 'GET':
            traveller_form = TravellerForm()
            
            return render(request,template_name,{'form':traveller_form})


        elif request.method == 'POST':
            traveller_form = TravellerForm(request.POST)
            
            if traveller_form.is_valid():
                origin = traveller_form.cleaned_data['origin']
                destination = traveller_form.cleaned_data['destination']
                print(origin, destination)
                day = traveller_form.cleaned_data['day']
                Traveller.objects.create(user=request.user, origin=origin, destination=destination, day=day)


                products=ProductBuyer.objects.filter(traveller=request.user.travellerUser);
                context = {
                'products': products,
                }


                return render(request, 'core/tchoose.html', context)
                
            return render(request,template_name)



def allocate(request):
    travellers = Traveller.objects.all()
    pbs = ProductBuyer.objects.order_by('timeOfOrder').filter(traveller=None)

    for trav in travellers:
        for pb in pbs:
            if((pb.product.location==trav.origin) and(pb.buyer.location==trav.destination) and (trav.itemsToBuy.count()<trav.maxAlloc)):
                trav.itemsToBuy.add(pb.product)
                pb.traveller = trav
                pb.save()

        trav.save()
    return redirect('core:home')



@login_required
def buyer(request, pno):
    if hasattr(request.user, 'buyerUser'):
        if pno is None:
            pno = 1;
        products = Product.objects.all();
        pno = int(pno)
        elementsPerPage = 8;
        # startItem = (pno-1)*elementsPerPage
        # finishItem = (pno)*elementsPerPage
        paginator = Paginator(products,elementsPerPage)
        
        limPro = paginator.get_page(pno)

        context = {
            'products' : limPro,
            'pno': pno,
            'totPages': range(1,paginator.num_pages+1) ,
            
        }
        if  pno<paginator.num_pages:
            context['nextPage'] =  pno+1

        if  pno>1:
            context['prevPage'] =  pno-1
            

        if not context['products']:
            return redirect('core:buyer') 
        
        return render(request, 'core/buyer.html', context)


    else:
        template_name = 'core/buyerform.html'

        if request.method == 'GET':
            buyer_form = BuyerForm()
            
            return render(request,template_name,{'form':buyer_form})


        elif request.method == 'POST':
            buyer_form = BuyerForm(request.POST)
            
            if buyer_form.is_valid():
                location = buyer_form.cleaned_data['location']
                print(location, "XXXXXXXXXXXXXXXXXXXXx")
                Buyer.objects.create(user=request.user, location=location)
                return redirect('core:buyer')
                
            return render(request,template_name)


        return redirect('core:home')



def loadProducts(request):
   
    products = []

    req = Request('https://www.leclos.net/shop/product-category/all/spirits/spirits-portfolio/', headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req).read()
    soup = bs4.BeautifulSoup(res,'html.parser')

    le = soup.select('.type-product')
    c=0;
    for el in le:
        if c > 7:
            break
        c = c+1
        imageUrl = el.select('.arrival-box')[0].img['src']
        name = el.select('.arrival-box-inner')[0].h3.a.get_text()[:42]
        price = el.select('.arrival-box-inner')[0].span.span.span.span
        price.extract()
        price = int(el.select('.arrival-box-inner')[0].span.span.span.get_text().strip().replace(',', ''))
        location = el.select('.arrival-box-inner .uk-breadcrumb li')[0].a.get_text()
        Product.objects.create(name= name, price= price, location= 'FR', imageUrl= imageUrl)
        products.append({'name': name, 'price': price, 'location': location, 'imageUrl': imageUrl})


    return redirect('core:buyer')


def addToCart(request):
    if request.method=="POST":
        id = int(request.POST.get('id'))
        product=Product.objects.get(id=id)
        quantity=request.POST.get('quantity')
        request.user.buyerUser.itemsInCart.add(product);
        ProductBuyer.objects.create(buyer=request.user.buyerUser, product=product, quantity=quantity)
        messages.success(request,f'Item has been Added to you Cart!')

        return redirect('core:cart')


def cart(request):
    # products=request.user.buyerUser.itemsInCart.all();
    products = ProductBuyer.objects.filter(buyer = request.user.buyerUser)
    context = {
    'products': products,
    }

    return render(request, 'core/cart.html', context)

def buyProd(request, id):
    if request.method=="POST":

        product=Product.objects.get(id=id)
        quantity=request.POST.get('quantity')
        ProductBuyer.objects.create(buyer=request.user.buyerUser, product=product, quantity=quantity)
        request.user.buyerUser.itemsInCart.remove(product)
        messages.success(request,f'Item bought Successfully!')

        return redirect('core:cart')




def wishlist(request):

    products=ProductBuyer.objects.filter(buyer=request.user.buyerUser);

    context = {
    'products': products,

    }

    return render(request, 'core/wishlist.html', context)



def tchoose(request):

    products=ProductBuyer.objects.filter(traveller=request.user.travellerUser);

    context = {
    'products': products,

    }

    return render(request, 'core/tchoose.html', context)




def checkout(request):
     # products=request.user.buyerUser.itemsInCart.all();
    products = ProductBuyer.objects.filter(buyer = request.user.buyerUser)
    total=[]
    for product in products:
        total.append(product.product.price*product.quantity)
    context = {
        'products': products,
        'total': total
    }
    return render(request, 'core/checkout.html',context)


def cartquantity(request):
    id = request.POST.get('id')
    q = int(request.POST.get('q'))
    pb = ProductBuyer.objects.get(id=id)
    print(q)
    pb.quantity = pb.quantity + q
    pb.save()
    return render(request, 'core/cart.html')


def deleteCart(request):
    id = request.POST.get('id')
    # q = int(request.POST.get('q'))
    ProductBuyer.objects.get(id=id).delete()
    products = ProductBuyer.objects.filter(buyer = request.user.buyerUser)
    context = {
        'products': products,
    }
    # print(q)
    # pb.quantity = pb.quantity + q
    # pb.save()
    return render(request, 'core/cart.html',context)

def buyerdelete(request):
    if hasattr(request.user, 'buyerUser'):
        Buyer.objects.get(user = request.user).delete()

    return redirect('core:home')



def travellerdelete(request):
    if hasattr(request.user, 'travellerUser'):
        Traveller.objects.get(user = request.user).delete()

    return redirect('core:home')