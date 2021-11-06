from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('books', views.ListBook.as_view(), name = 'books'),
    path('books/<int:pk>', views.DetailBook.as_view(), name = 'book'),
    path('products', views.ListProduct.as_view(), name = 'Products'),
    path('products/<int:pk>', views.DetailProduct.as_view(), name = 'product'),
    path('signup', views.CreateSkartUser.as_view(), name='user'),
    path('login/', TokenObtainPairView.as_view(), name= 'user_token_obtain'),
    path('refreshtoken/', TokenRefreshView.as_view(), name= 'refresh_token'),
    path('myprofile/<int:pk>', views.SkartUserProfile.as_view(), name= 'myprofile'),
    path('myprofile/cart', views.CartView.as_view(), name= 'Cart'),
    path('myprofile/cart/<int:pk>', views.CartUpdateView.as_view(), name = 'my_cart'),
    path('myprofile/cart/r/<int:pk>', views.RemoveItemsCartView.as_view(), name = 'remove_itmes_from_cart'),
    path('myprofile/placeorder', views.PlaceOrderView.as_view(), name = 'place_order'),
    path('myprofile/order/<int:pk>', views.ItemsCancelOrderView.as_view(), name = 'Items_cancel_order'),

]