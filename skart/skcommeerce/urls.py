from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('products', views.ListProduct.as_view(), name='Products'),
    path('products/<int:pk>', views.DetailProduct.as_view(), name='product'),
    path('customer/signup', views.CreateCustomerView.as_view(),
         name='customer_signup'),
    path('login/', TokenObtainPairView.as_view(), name='user_token_obtain'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='refresh_token'),
    path('customerprofile/<int:pk>',
         views.CustomerProfile.as_view(), name='customer_profile'),
    path('seller/signup', views.CreateSellerView.as_view(), name='seller_signup'),
    path('sellerprofile/<int:pk>',
         views.SellerProfile.as_view(), name='seller_profile'),
    path('sellerprofile/update/<int:pk>',
         views.UpdateSellerProfile.as_view(), name='update_seller_profile'),
    path('myprofile/cart/<int:pk>', views.CartUpdateView.as_view(), name='my_cart'),
    path('myprofile/cart/r/<int:pk>', views.CartRemoveView.as_view(),
         name='cancel_products_in_cart'),
    path('myprofile/order', views.PlaceOrderView.as_view(), name='place_order'),
    path('myprofile/order/<int:pk>',
         views.ItemsCancelOrderView.as_view(), name='Items_cancel_order'),
    path('myprofile/cancelorder',
         views.CancellOrderView.as_view(), name='cancel_order'),
    path('myprofile/cancelorder/<int:pk>',
         views.RetrieveCancelledOrderView.as_view(), name='cancelled_order'),
    path('myprofile/products', views.ListCreateProductView.as_view(),
         name='list_and_create_products'),
    path('myprofile/products/<int:pk>', views.RetrieveUpdateDestroyProductsView.as_view(),
         name='retrieve_update_destroy_products'),

]
