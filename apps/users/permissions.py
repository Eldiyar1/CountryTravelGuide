from rest_framework import permissions


class NotificationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'
