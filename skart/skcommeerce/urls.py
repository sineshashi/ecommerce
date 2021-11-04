from django.urls import path, include
from . import views
# from rest_framework_ import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('books', views.ListBook.as_view(), name = 'books'),
    path('books/<int:pk>', views.DetailBook.as_view(), name = 'book'),
    path('products', views.ListProduct.as_view(), name = 'Products'),
    path('products/<int:pk>', views.DetailProduct.as_view(), name = 'product'),
    path('sign-up', views.CreateSkartUser.as_view(), name='user'),
    # path('log-in/', TokenObtainPairView.as_view(), name= 'user_token_obtain'),
    path('myprofile/', views.UpdateSkartUser.as_view(), name= 'myprofile')
]