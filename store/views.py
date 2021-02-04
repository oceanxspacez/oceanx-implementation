from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
# from store code
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.template import loader
# from .forms import RegisterForm
from django import template
from .models import *
from . import forms
#Cnotes - allow us to send to email
from django.core.mail import send_mail

#Cnotes - django utility function to quickly logout might need to change this one if we have time
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'store/signup.html'


# Starting Code for the store
#Cnotes - this will allow us to call/render the html file booking 
def booking(request):
        if request.method == "POST":
            your_name = request.POST['your-name']
            your_phone = request.POST['your-phone']
            your_email = request.POST['your-email']
            your_address = request.POST['your-address']
            your_service = request.POST['your-service']
            your_date = request.POST['your-date']
            your_schedule = request.POST['your-schedule']
            your_message = request.POST['your-message']
            
            #Cnotes - this sends to email
            booking = "Name: " + your_name + " Phone: " + your_phone + " Email: " + your_email + " Address: " + your_address + " Time: " + your_schedule + " Date: " + your_date + " Message: " + your_message

            send_mail(
                    'Booking Request', # subject
                    booking, # message
                    your_email, # from email
                    ['oceanxspacez@gmail.com'], # to email
                )

            #review customer booking    
            return render(request, 'store/booking.html', {
                    'your_name' : your_name,
                    'your_phone' : your_phone,
                    'your_email' : your_email,
                    'your_address' : your_address,
                    'your_service' : your_service,
                    'your_date' : your_date,
                    'your_schedule' : your_schedule,
                    'your_message' : your_message
                    })
                
        else:
                return render(request, 'store/booking.html', {})
                
    

def loginView(request):
    return render(request, 'registration/login.html')


def store(request):

        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        #Cnotes - we get all the data of Product from the database
        products = Product.objects.all()
        context = {'products':products, 'cartItems':cartItems}
        return render(request, 'store/store.html', context)

def cart(request):

        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        context = {'items':items, 'order':order, 'cartItems':cartItems}
        return render(request, 'store/cart.html', context)
#CodeNotes - this renders checkout html with the data from the cart
def checkout(request):

        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        context = {'items':items, 'order':order, 'cartItems':cartItems}
        return render(request, 'store/checkout.html', context)
#CodeNotes - function that allows logged in users to view  if data is added or not
def updateItem(request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added', safe=False)
#Cnotes processes the order to the checkout. it is also
def processOrder(request):
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
                customer = request.user.customer
                order, created = Order.objects.get_or_create(customer=customer, complete=False)

        else:
                customer, order = guestOrder(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
                order.complete = True
        order.save()

        if order.shipping == True:
                ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=['shipping']['address'],
                city=['shipping']['city'],
                postalcode=['shipping']['postalcode'],
                suburb=['shipping']['suburb'],
                )

        return JsonResponse('Payment submitted..', safe=False)
