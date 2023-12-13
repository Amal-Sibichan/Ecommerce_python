from django.shortcuts import render,redirect
from django.http import HttpResponse
import razorpay
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from.models import Userdetails,Address,Seller,Product, Image, Size,Category,Cart,Order
from django.db.models import Q 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import razorpay
from django.views.decorators.csrf import csrf_exempt
import re
from django.utils import timezone


def index(request):
    products = Product.objects.all().order_by('date')

  
    product_data = []

    for product in products:
        try:
            
           image = Image.objects.filter(product=product).first()
           image_url = image.image.url if image else None
        except Image.DoesNotExist:
            
            image_url = None

        
        product_data.append({
            'product': product,
            'image_url': image_url,
        })

    products_per_page = 4
    paginator = Paginator(product_data, products_per_page)
    page = request.GET.get('page')

    try:
        product_data = paginator.page(page)
    except PageNotAnInteger:
        
        product_data = paginator.page(1)
    except EmptyPage:
        
        product_data = paginator.page(paginator.num_pages)    

    
    context = {'product_data': product_data}

    return render(request,'index.html',context)



def cart(request):
    if 'profile' in request.session:
        user_email = request.session.get('profile')
        user = Userdetails.objects.get(email=user_email)

        
        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:

            first_image = item.product.image_set.first()
            
            
            item.image_url = first_image.image.url if first_image else None

            item.total_amount = item.quantity * item.product.price

        
        cart_total = sum(item.total_amount for item in cart_items)
        
        

        context = {
            'cart_items': cart_items,
            'cart_total': cart_total,
            
        }

        return render(request, 'cart.html', context)

    return render(request, 'cart.html')
    



    

def grid(request):
    products = Product.objects.all().order_by('date')

   
    product_data = []

    for product in products:
        try:
            
           image = Image.objects.filter(product=product).first()
           image_url = image.image.url if image else None
        except Image.DoesNotExist:
           
            image_url = None
        stock = product.quantity >= 1

       
        product_data.append({
            'product': product,
            'image_url': image_url,
            'stock':stock,
        })

    products_per_page = 9

    paginator = Paginator(product_data, products_per_page)
    page = request.GET.get('page')

    try:
        product_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        product_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        product_data = paginator.page(paginator.num_pages)    

    # Pass the product data to the template
    context = {'product_data': product_data}
    return render(request, 'shop-grid.html', context)





def add_to_cart(request):
   if 'profile' in request.session:
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user_email = request.session.get('profile')
        user = Userdetails.objects.get(email=user_email)
        size_name = request.POST.get('size')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(product_id=product_id)

        first_image = product.image_set.first()

            # Check if the product has an image
        if first_image:
                # Get the image URL
                image_url = first_image.image.url
        else:
                # If no image is found, you can set a default image or handle it as needed
                image_url = 'path/to/default/image.jpg'



        price = product.price 
        total = price * int(quantity)

        print(price)
        print(total)

        # Create a Cart instance and save it
        cart_item = Cart.objects.create(
            user=user,
            product=product,
            size=size_name,
            quantity=quantity,
            price=total,
            image=image_url,
        )

        

        # You can perform additional operations here, like updating quantities if the item already exists

        return redirect('cart')  # Redirect to the cart page or any other desired page
    
    return render(request, 'product_details.html') 
   return render(request, 'Ulogin.html')
    
   



def delete_cart_item(request, cart_item_id):
    if 'profile' in request.session:
        user_email = request.session.get('profile')
        user = Userdetails.objects.get(email=user_email)

        # Retrieve the cart item to delete
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=user)

        # Delete the cart item
        cart_item.delete()

        return redirect('cart')

    return render(request, 'cart.html')



def product_details(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    sizes = Size.objects.all()
    stock = product.quantity >=1
    print(stock)


    # Get the related images for the product
    images = Image.objects.filter(product=product)

    context = {'product': product, 'images': images, 'sizes': sizes,'stock':stock}
    return render(request, 'product_details.html', context)




def contact(request):
    return render(request,'contact.html')



def proceed(request):
  if 'profile' in request.session:
    user_email = request.session.get('profile')
    pstatus = request.POST.get('pstatus')
    # Check if the user is logged in (you can customize this logic based on your authentication mechanism)
    if user_email:
        # Fetch user details using the provided email
        user = Userdetails.objects.get(email=user_email)

        dte= timezone.now().date()

        # Check if the user has an address
        address = user.address_set.first()

        if not address:
            # Redirect the user to add an address if none exists
            return redirect('add_address')

        # Get the user's cart items
        cart_items = Cart.objects.filter(user=user)

        # Create orders for each cart item
        for item in cart_items:
            order = Order.objects.create(
                user=user,
                product=item.product,
                size=item.size,
                quantity=item.quantity,
                price=item.price,
                image=item.image,
                status='Pending',
                date =dte,
                pstatus=pstatus
            )

        
        product = item.product
        product.quantity -= item.quantity
        product.save()
       

            
        # Clear the user's cart after creating orders
        cart_items.delete()

        return redirect('uprofile')

    else:
        # Handle the case where the user email is not in the session
        return redirect('userlogin')




client = razorpay.Client(auth=('rzp_test_t1badRwbKEAa0y', 'sknIQ6rjFkal9zQJvBIkbAmN'))
def pay(request):

     if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000

        client = razorpay.Client(auth=('rzp_test_t1badRwbKEAa0y', 'sknIQ6rjFkal9zQJvBIkbAmN'))

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
     return render(request, 'checkout.html')
  

@csrf_exempt
def success(request):
    name = request.POST.get('name')
    home = request.POST.get('home')
    street = request.POST.get('street')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip_code')

    context = {'name': name,'home':home,'street':street,'city':city,'zip_code':zip_code,'state':state}
    return render(request, "card_payment.html",context)





def checkout(request):
    if 'profile' in request.session:
        user_email = request.session.get('profile')
        user = Userdetails.objects.get(email=user_email)
        name= user.firstname
        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:

            item.total_amount = item.quantity * item.product.price

        # Calculate the total price for all items in the cart
        cart_total = sum(item.total_amount for item in cart_items)
        pay = cart_total * 100
        # Check if the user has an address
        address_exists = Address.objects.filter(email=user).exists()
        

        if address_exists:
            # If the user has an address, retrieve and display it
            address = Address.objects.get(email=user)
            context = {'address': address,'cart_total':cart_total ,'name': name,'pay':pay}
        else:
            # If the user doesn't have an address, redirect to the add address page
            return redirect('add_address')

        # Add other necessary context data and logic for checkout

        return render(request, 'checkout.html', context)

    return render(request, 'checkout.html')





def s_register(request):

     if request.method == 'POST':
        name=request.POST['seller_name']
        email=request.POST['email']
        phone=request.POST['phone']
        company=request.POST['companyname']
        address=request.POST['address']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if len(phone) !=10:
            messages.info(request, 'enter a valid mobile number.')
            return redirect('sellerregister') 
      
        if not (len(password1) >= 8 and re.search(r'[a-zA-Z]', password1) and re.search(r'\d', password1)):
            messages.info(request, 'Password should be at least 8 characters long and contain at least one letter and one digit.')
            return redirect('sellerregister')

        if password1==password2:

            if Seller.objects.filter(email=email).exists():
                messages.info(request,'email taken....')
                return redirect('sellerregister')
            elif Seller.objects.filter(company_name=company).exists():
                messages.info(request,'company name alredy exists.....')
                return redirect('sellerregister')  

            else:

                seller = Seller(seller_name=name,email=email,company_name=company,address=address,phone=phone,password=password1)
                seller.save();
                print("user registered")
                return redirect('sellerlogin')

        else:
            messages.info(request,'password not matching!...')
            return redirect('sellerregister')    
        

     else:
 
       
       return render(request,'Sregister.html')
     

 


def register(request):
    if request.method == 'POST':
        name=request.POST['firstname']
        email=request.POST['email']
        phone=request.POST['phone']
        password1=request.POST['password1']
        password2=request.POST['password2']


      
        if len(phone) !=10:
            messages.info(request, 'enter a valid mobile number.')
            return redirect('register') 
      
        if not (len(password1) >= 8 and re.search(r'[a-zA-Z]', password1) and re.search(r'\d', password1)):
            messages.info(request, 'Password should be at least 8 characters long and contain at least one letter and one digit.')
            return redirect('register')

        if password1==password2:

            if Userdetails.objects.filter(email=email).exists():
                messages.info(request,'email taken....')
                return redirect('register')
               

            else:

                seller = Userdetails(firstname=name,email=email,phone=phone,password=password1)
                seller.save();
                print("user registered")
                return redirect('userlogin')

        else:
            messages.info(request,'password not matching!...')
            return redirect('register')    
        

    else:

       return render(request,'uregister.html')
    





def ulog(request):
    if 'profile' in request.session:
     return render(request,'index.html')

    else:
          if (request.method == 'POST'):
              email=request.POST['email']
              password=request.POST['password']

              if Userdetails.objects.filter(email=email):
                data = Userdetails.objects.get(email=email)
                if (data.password == password):
                  request.session['profile']=data.email
                  return redirect('index')
                else:
                  messages.error(request,'wrong username or password')
                  return redirect('userlogin')
              else:
                messages.error(request,'wrong username or password.')
                return redirect('userlogin')
          else:
             return render(request,'Ulogin.html')
          







def slog(request):

    if 'seller' in request.session:
     return render(request,'sellerhome.html')

    else:
          if (request.method == 'POST'):
              email=request.POST['email']
              password=request.POST['password']

              if Seller.objects.filter(email=email):
                data = Seller.objects.get(email=email)
                if (data.password == password):
                  request.session['seller']=data.id
                  print('logged as seller' )
                  return redirect('sellerhome')
                else:
                  messages.error(request,'wrong email or password')
                  return redirect('sellerlogin')
              else:
                messages.error(request,'wrong email or password.')
                return redirect('sellerlogin')
          else:
             return render(request,'Slogin.html')
          





   
def shome(request):
   if 'seller' in request.session:
     seller_id = request.session['seller']

     if seller_id:
        # Fetch products uploaded by the seller
        products = Product.objects.filter(seller=seller_id)
        print(products)

        # Create a list to store product details and associated images
        product_data = []

        for product in products:
            # Get the first related image for the product
            image = Image.objects.filter(product=product).first()
            image_url = image.image.url if image else None

            # Append product details and image URL to the list
            product_data.append({
                'product': product,
                'image_url': image_url
            })

        # Pass the product data to the template
        context = {'product_data': product_data}
        return render(request, 'sellerhome.html', context)
   else:
      return redirect('sellerlogin')
   






def add(request):
     if request.method == 'POST':
        # Get form data from POST request
        product_name = request.POST.get('product_name')
        discription = request.POST.get('discription')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        sizes = request.POST.getlist('sizes')  # Assuming sizes is a multiple-choice field in your form
        images = request.FILES.getlist('images')
        selected_category = request.POST.get('category_select')

        # Fetch the seller based on the seller_id session key
        seller_id = request.session.get('seller')

        try:
            seller = Seller.objects.get(id=seller_id)
        except ObjectDoesNotExist:
            # Handle the case where the seller does not exist (optional)
            return render(request, 'error_page.html', {'error_message': 'Seller does not exist.'})
        
        categories = Category.objects.all()

        # Create the product
        product = Product.objects.create(
            seller=seller,
            product_name=product_name,
            discription=discription,
            price=price,
            quantity=quantity
        )

        # Add sizes to the product
        size_objects = [Size.objects.get_or_create(size_name=size)[0] for size in sizes]
        product.sizes.set(size_objects)

        if selected_category:
            try:
                category = Category.objects.get(category_id=selected_category)
                print(category)
                product.category = category
                product.save()
            except Category.DoesNotExist:
                # Handle the case where the category does not exist (optional)
                return render(request, 'error_page.html', {'error_message': 'Category does not exist.'})

        # Handle images
        for image in images:
            Image.objects.create(product=product, image=image)

        return redirect('sellerhome')  
     categories = Category.objects.all()
     return render(request, 'add.html', {'categories': categories})




def address(request):
    user_email = request.session.get('profile')

    if not user_email:
        return redirect('Slogin')  #
    user = get_object_or_404(Userdetails, email=user_email)

    # Check if the user already has an address
    address_exists = Address.objects.filter(email=user).exists()

    if not address_exists and request.method == 'POST':
        # Process the form submission
        home = request.POST.get('home')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        # Create a new address for the user
        Address.objects.create(
            email=user,
            home=home,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )

        # Redirect to the user profile or any other desired page
        return redirect('uprofile')  # Change 'user_profile' to your actual user profile URL

    return render(request, 'address.html', {'user_email': user_email, 'address_exists': address_exists})

    




def uprof(request):
    if 'profile' in request.session:
  
        email = request.session['profile']

        try:
            user_details = Userdetails.objects.get(email=email)
        except Userdetails.DoesNotExist:
            # Handle the case where the user with the provided email does not exist
            return redirect('userlogin')

        try:
            user_address = Address.objects.get(email=user_details)
        except Address.DoesNotExist:
            user_address = None

        orders = Order.objects.filter(user=user_details)

        return render(request, 'Uprofile.html', {'view_user_details': user_details, 'view_user_address': user_address, 'orders': orders})
    else:
        return redirect('userlogin')






def sprof(request):
    if 'seller' in request.session:
        id = request.session['seller']
        pending_orders = Order.objects.all().order_by('date')

        # Create a list to store order details for rendering in the template
        order_details = []

        for order in pending_orders:
            # Get user details
            user_details = order.user
            user_address = get_object_or_404(Address, email=user_details)

            # Get product details
            product = get_object_or_404(Product, pk=order.product_id)
            product_image = Image.objects.filter(product=product).first()
            image = product_image.image.url
            seller = get_object_or_404(Seller, pk=product.seller_id)

            # Calculate total price
            total_price = order.price / order.quantity

            order_details.append({
                'order': order,
                'user_details': user_details,
                'user_address': user_address,
                'product': product,
                'seller': seller,
                'total_price': total_price,
                'image': image,
            })

        return render(request, 'Sprofile.html', {'order_details': order_details})
    else:
        return redirect('sellerlogin')



def accept_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            # Update the status of the order to 'Accepted' or any other desired status
            order = Order.objects.get(id=order_id)
            dte= timezone.now().date()

            if order.status == 'Pending':
              order.status = 'dispatched'
            elif order.status == 'dispatched':
              order.status = 'On the way'
            elif order.status == 'On the way':
              order.status = 'Delivered'
            order.date=dte
            order.save()

    return redirect('sprofile') 




def on(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            # Update the status of the order to 'Accepted' or any other desired status
            order = Order.objects.get(id=order_id)
            
            if order.status == 'Ordered':
             order.status = 'Dispatched'
            elif order.status == 'Dispatched':
             order.status = 'On the way'
            elif order.status == 'On the way':
             order.status = 'Delivered'


    return redirect('sprofile')



def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Add any additional logic to fetch tracking details if needed
    return render(request, 'tracking.html', {'order': order})

def search_view(request):
     query = request.GET.get('query', '')
     category = request.GET.get('category', '')
     products = Product.objects.filter(
        Q(product_name__icontains=query) |
        Q(discription__icontains=query) |
        Q(seller__seller_name__icontains=query) |
        Q(price__icontains=query) |
        Q(category__category_name__icontains=query),
         category__category_name__icontains=category  # Add more fields as needed
    ).distinct()

     product_data = []

     for product in products:
        try:
            image = Image.objects.filter(product=product).first()
            image_url = image.image.url if image else None
        except Image.DoesNotExist:
            image_url = None

        product_data.append({
            'product': product,
            'image_url': image_url,
        })
     products_per_page = 9

     paginator = Paginator(product_data, products_per_page)
     page = request.GET.get('page')

     try:
        product_data = paginator.page(page)
     except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        product_data = paginator.page(1)
     except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        product_data = paginator.page(paginator.num_pages)  

     context = {'product_data': product_data, 'query': query,'category': category}
     return render(request, 'search.html', context)

def logout_u(request):
    logout(request)
    return redirect('index')

def logout_s(request):
    logout(request)
    return redirect('sellerlogin')



