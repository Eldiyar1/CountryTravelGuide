from rest_framework import permissions


class OnlyGet(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return False


class KitchenPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_kitchen
        else:
            return True if request.method == 'GET' else False


class MenuPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.kitchen.user == request.user:
            return True
        else:
            return True if request.method == 'GET' else False

