from django.contrib import admin
from .models import *

# Register your models here.
#CNotes - any added models here should be migratrated in the terminal otherwise they wont show in the django admin
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
