from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'store'
# Cnotes - fixed the url errors by commenting app_name and changing the urls in the base.html. from: store:store to just store 

urlpatterns = [

# Codes starting for the store part
    #Cnotes - leave empty for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('booking/', views.booking, name="booking"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

    path('login/',auth_views.LoginView.as_view(template_name='store/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),

]
