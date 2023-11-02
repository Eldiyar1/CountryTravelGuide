from rest_framework import permissions


class OnlyGet(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or view.action == 'subscribe':
            return True
        else:
            return False


class KitchenPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'add_rating':
            return True
        else:
            return True if request.method == 'GET' else request.user.is_kitchen


class MenuPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.kitchen.user == request.user:
            return True
        else:
            return True if request.method == 'GET' else False

