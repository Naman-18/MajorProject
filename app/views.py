from time import time
from django.contrib.auth import login
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from numpy.core.fromnumeric import prod
from .models import TempImage,Customer, Product, Cart, OrderPlaced, Wishlist, Reviews
from .forms import CustomerRegistrationForm, CustomerProfileForm, CustomerReviewForm, OrderPlacedForm,ProductForm, ImageSearchForm, TempForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import warnings
import csv
from datetime import date
from datetime import datetime,date
from datetime import timedelta
from base64 import b64encode

warnings.filterwarnings('ignore')


def append_data(sales):
    today = date.today()
    lastrow = []
    allRows = []
    with open("test.csv","r") as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            lastrow = row
            allRows.append(row)
    
    if lastrow[1] == str(today):
        newSales = int(allRows[-1][4]) + sales
        allRows[-1][4]  = str(newSales)
        with open("test.csv","a") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(allRows)
            csvfile.close()
    else:
        nextRow = []
        nextRow.append(str(int(lastrow[0])+1))
        nextRow.append(str(today))
        nextRow.append(lastrow[2])
        nextRow.append(lastrow[3])
        nextRow.append(str(sales))
        nextRow.append(str(today.year))
        nextRow.append(str(today.month))
        nextRow.append(str(today.day))
        nextW = int(lastrow[-1])+1
        if nextW > 7:
            nextW = 1
        nextRow.append(str(nextW))

        with open("test.csv","a") as csvfile:
            writerObj = csv.writer(csvfile)
            writerObj.writerow(nextRow)
            csvfile.close()


class ProductView(View):
    def get(self,request):
        totalitem=0
        acoustic = Product.objects.filter(category = 'AG')
        electric = Product.objects.filter(category = 'EG')
        classical = Product.objects.filter(category = 'CG')
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',
        {'acoustic':acoustic, 'electric' : electric, 'classical': classical,'totalitem':totalitem})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')




class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        product = Product.objects.get(pk=pk)
        reviews = Reviews.objects.filter(product= product)
        item_already_in_cart =False
        
        if(request.user.is_authenticated):
            item_already_in_cart = Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
            if request.user.is_authenticated:
             totalitem= len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html',
            {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem,'reviews':reviews})

@login_required
def add_to_cart(request):

 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()

 return redirect('/cart')

def searchproduct(request):
    query = request.GET.get('search_query')
    find_product = Product.objects.filter(
        Q(title__icontains=query)|
        Q(brand__icontains=query)|
        Q(category__icontains=query)|
        Q(description__icontains=query)
    )
    return render (request,'app/searchresults.html',{'search_query':query,'match_product':find_product})

def searchproductimage(request):
    if request.method == 'POST':
        form = ImageSearchForm(request.POST, request.FILES)
        if form.is_valid():
            # prod_image = request.FILES['image']
            # form = ImageSearchForm()
            # data = prod_image.read()
            # # Calling .decode() converts bytes object to str
            # encoded = b64encode(data).decode()
            # mime = 'image/jpeg;'
            # context = {"image": "data:%sbase64,%s" % (mime, encoded)}
            records = TempImage.objects.all()
            records.delete()
            imgForm = TempForm(request.POST,request.FILES)
            if imgForm.is_valid():
                imgForm.save()
                records = TempImage.objects.get()
                image = records.image
                # print(image.url)
                # print(records.image)
            # image = form.cleaned_data['image']
            # b64_img = b64encode(image.file.read())
            # print(records)
            return render(request, 'app/imagesearchresults.html', {'form':form, 'image':image})
    else:
        form = ImageSearchForm()
    return render (request,'app/imagesearchresults.html',{'form':form})

@login_required
def add_to_wishlist(request):
    user= request.user
    product_id = request.GET.get('prod_id')
    product  =Product.objects.get(id=product_id)
    Wishlist(user=user,product=product).save()
    return redirect('/wishlist')

def show_wishlist(request):
    if request.user.is_authenticated:
        totalitem=0
        user =request.user
        wish = Wishlist.objects.filter(user=user)
        if request.user.is_authenticated:
             totalitem= len(Cart.objects.filter(user=request.user))
     
        return render(request,'app/wishlist.html',{'wish':wish,'totalitem':totalitem})

def deletewishlist(request):
    wishid = request.GET.get('wishlistid')
    c =Wishlist.objects.get(Q(id=wishid) & Q(user=request.user))
    c.delete()
    return redirect ('/wishlist')     

def deletereview(request):
    viewid = request.GET.get('reviewid')
    c =Reviews.objects.get(Q(id=viewid) & Q(user=request.user))
    c.delete()
    return  redirect('/orders')


@login_required
def buynow(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    quantity=1
    Cart(user=user,product=product,quantity=quantity).save()
    return redirect('/checkout')

@method_decorator(login_required,name='dispatch')
class ReviewView(View):
    def get(self,request):
        product_id = request.GET.get('prod_id')
        reviewproduct = Product.objects.get(id=product_id)
        form = CustomerReviewForm()
        return render(request,'app/addreview.html',{'product':reviewproduct,'form':form})
    
    def post(self,request):
        form =CustomerReviewForm(request.POST)
        if form.is_valid():
            user = request.user
            product_id = request.GET.get('prod_id')
            product = Product.objects.get(id=product_id)
            description = form.cleaned_data['description']
            reviews = Reviews.objects.filter(product= product)
            reviews_count = len(reviews)

            data = pd.read_excel("review-details.xlsx")
            T_data = data[['review_text', 'review_rating']]
            df = T_data 
            df1 = df.dropna()
            df1.head()   
            df1['Cleaned'] = df1['review_text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
            df1['Cleaned'] = df1['Cleaned'].str.replace('[^\w\s]','')
            
            x = df1['Cleaned']       
            y = df1['review_rating']
            tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(1,2), max_features=10000)
            tfidf_vect_ngram.fit(x)
            
            Model = joblib.load('F_model_retpred.sav')
            new_review = description

            padded = tfidf_vect_ngram.transform([new_review])
            ALL = Model.predict(padded)
            
            #print("Product Rating:",ALL)
            #print(product.rating)
            cur = 0
            print(product.rating)
            if product.rating != None:
                cur = product.rating
            temp_rating = (cur*reviews_count)+ALL
            temp_count = reviews_count+1
            #print(temp_rating)

            print(temp_rating,temp_count,cur)
            product.rating = temp_rating/temp_count
            product.save()
            #print(product.rating)
            reg = Reviews(user=user,description=description,product =product)
            reg.save()
            messages.success(request, 'Review Added Successfully')
            totalitem=0
            acoustic = Product.objects.filter(category = 'AG')
            electric = Product.objects.filter(category = 'EG')
            classical = Product.objects.filter(category = 'CG')
            if request.user.is_authenticated:
                totalitem= len(Cart.objects.filter(user=request.user))
            return render(request, 'app/home.html',
            {'acoustic':acoustic, 'electric' : electric, 'classical': classical,'totalitem':totalitem})
            

 
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        totalitem=0
        user =request.user
        cart = Cart.objects.filter(user=user)
        if request.user.is_authenticated:
             totalitem= len(Cart.objects.filter(user=request.user))
        amount= 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount+=tempamount
            total_amount = amount+shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'amount':amount,'shipping': shipping_amount,'totalamount':total_amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c =Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount= 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+=tempamount
        total_amount = amount+shipping_amount
        data ={'quantity':c.quantity, 'amount':amount,'totalamount':total_amount}
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c =Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount= 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+=tempamount
        total_amount = amount+shipping_amount
        data ={'quantity':c.quantity, 'amount':amount,'totalamount':total_amount}
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c =Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount= 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+=tempamount
        total_amount = amount+shipping_amount
        data ={'amount':amount,'totalamount':total_amount}
        return JsonResponse(data)

#def buy_now(request):
 #return render(request, 'app/buynow.html')

#def profile(request):
 #return render(request, 'app/profile.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form, 'active':'btn-secondary'})
    
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Address Added Successfully')
        return render(request,'app/profile.html',{'form':form, 'acitve':'btn-secondary'})

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-secondary'})

def deleteaddress(request):
    custid = request.GET.get('addid')
    c =Customer.objects.get(Q(id=custid) & Q(user=request.user))
    c.delete()
    return redirect ('/address')


@login_required
def orders(request):
    orders = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'orders':orders})

@login_required
def change_password(request):
    return render(request, 'app/changepassword.html')

def acousticguitar(request,data=None):
    if data == None:
        guitar = Product.objects.filter(category='AG')
    elif data == 'Fender' or data == 'Cort' or data == 'Yamaha':
        guitar = Product.objects.filter(category='AG').filter(brand=data)
    elif data == 'below':
        guitar = Product.objects.filter(category='AG').filter(discounted_price__lt = 10000)
    elif data == 'above':
        guitar = Product.objects.filter(category='AG').filter(discounted_price__gt = 10000)
    return render(request, 'app/acousticguitar.html',{'guitar':guitar})

def electricguitar(request,data=None):
    if data == None:
        guitar = Product.objects.filter(category='EG')
    elif data == 'Fender' or data == 'Cort' or data == 'Ibanez' or data=='ESP':
        guitar = Product.objects.filter(category='EG').filter(brand=data)
    elif data == 'below':
        guitar = Product.objects.filter(category='EG').filter(discounted_price__lt = 10000)
    elif data == 'above':
        guitar = Product.objects.filter(category='EG').filter(discounted_price__gt = 10000)
    return render(request, 'app/electricguitar.html',{'guitar':guitar})

def classicalguitar(request,data=None):
    if data == None:
        guitar = Product.objects.filter(category='CG')
    elif data == 'Fender' or data == 'Cort' or data == 'Ibanez' or data =='Yamaha' or data=='Epiphone' or data=='Valencia':
        guitar = Product.objects.filter(category='CG').filter(brand=data)
    elif data == 'below':
        guitar = Product.objects.filter(category='CG').filter(discounted_price__lt = 10000)
    elif data == 'above':
        guitar = Product.objects.filter(category='CG').filter(discounted_price__gt = 10000)
    return render(request, 'app/classicalguitar.html',{'guitar':guitar})

#def login(request):
# return render(request, 'app/login.html')

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Registered Successfully')
            form.save()

        return render(request, 'app/customerregistration.html',{'form':form})


@login_required
def checkout(request):
    totalitem=0
    user =request.user
    add =Customer.objects.filter(user = user)
    cart_items = Cart.objects.filter(user=user)
    amount= 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    total_quantity = 0
    for p in cart_product:
        if p.quantity<1:
            p.delete()
        else:
            total_quantity += p.quantity
    
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+=tempamount
        total_amount = amount+shipping_amount
        append_data(total_quantity)
        return render(request, 'app/checkout.html',{'add':add, 'totalamount':total_amount, 'cart_items':cart_items,'totalitem':totalitem})
    
    else:
        return render(request,'app/emptycart.html')

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user = user)
    if cart:
        for c in cart:
            OrderPlaced(user=user, customer=customer,product=c.product, quantity=c.quantity).save()
            c.delete()
        return redirect("orders")
    else:
        return render(request,'app/emptycart.html')

# Admin Views

def dashboard(request):
    totalOrders = OrderPlaced.objects.filter().__len__()
    deliveredOrders = OrderPlaced.objects.filter(status = "Delivered").__len__()
    pendingOrders = OrderPlaced.objects.filter(status = "Pending").__len__()
    allOrders = OrderPlaced.objects.all()
    return render(request,"app/admin-dashboard.html",{
        "total":totalOrders,
        "pending":pendingOrders,
        "delivered":deliveredOrders,
        "orders":allOrders,
    });

def addProduct(request):
    products = Product.objects.all()
    return render(request,"app/AddProduct.html",{
        "products":products,
    })
def createProduct(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES["product_image"])
        form = ProductForm(request.POST,request.FILES) 
        if form.is_valid():
            form.save()
        else:       
            print(form.errors)
    return redirect("add-product")
def updateProduct(request,pk):
    print(pk)
    order = OrderPlaced.objects.get(id=pk)
    if request.method == "POST":
        form = OrderPlacedForm(request.POST,instance = order)
        if form.is_valid():
            form.save()
            return redirect("/Admin/dashboard")
        else:
            print(form.error)
        
    return render(request,"app/adminupdateProduct.html",{
        "order":order
    })
def salesForecasting(request):
    lim = 1000
    graphType = "bar"
    if request.method == "POST":
        if request.POST["duration"] != "50 +": 
            lim = int(request.POST["duration"])
        graphType = str(request.POST["graph"]).lower()
    train_df = pd.read_csv("train.csv")
    test_df = pd.read_csv("test.csv")
    arima_test_df = test_df[['date','sales']].set_index('date')
    arima_df = train_df[['date','sales']].set_index('date')
    arima_test_df = arima_test_df['sales'].astype(int)
    model = joblib.load("forecastingModel.sav");
    predSales = model.predict(start=arima_test_df.index[0], end=arima_test_df.index[-1], dynamic= True)
    sales = []
    dates = []
    current = str(date.today())
    today = datetime.strptime(current,"%Y-%m-%d")
    ctr = 0
    for i in predSales:
        if ctr >= lim:
            break
        else:
            sales.append(int(i))
            ctr = ctr+1
    ctr = 0
    for i in range(1,len(sales)+1):
        if ctr >= lim:
            break
        else:
            nextdate = today + timedelta(i)
            inserteddate = str(nextdate).split(' ')[0]
            # print(inserteddate)
            dates.append(inserteddate)
            ctr = ctr+1
    # print(len(sales),len(dates))
    return render(request,"app/SalesForecasting.html",{
        "sales":sales,
        "dates":dates,
        "graph":graphType,
    })