from rest_framework.exceptions import NotAcceptable, NotAuthenticated
from rest_framework.permissions import BasePermission
from .models import Seller, Customer
from rest_framework.response import Response
from rest_framework import status
class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if Seller.objects.filter(user_id = request.user.id).first() is None:
            raise NotAuthenticated("You are not authorized for this action.")
        return bool(request.user and request.user.is_staff)
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if Customer.objects.filter(user_id = request.user.id).first() is None:
            raise NotAuthenticated("You are not authorized for this action.")
        return bool(request.user and request.user.is_authenticated)


