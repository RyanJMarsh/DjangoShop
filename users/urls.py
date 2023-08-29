from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('myitems/', views.myitems, name='myitems'),
    path('myitems/order_detail/<int:pk>/', views.myitems_order_detail, name='myitems_order_detail'),
    path('myitems/add-item/', views.add_item, name='add_item'),
    path('myitems/edit-item/<int:pk>/', views.edit_item, name='edit_item'),
    path('myitems/delete-product/<int:pk>/', views.delete_item, name='delete_item'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail')
]