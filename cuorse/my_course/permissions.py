from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CheckOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class CheckExam(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "student"
