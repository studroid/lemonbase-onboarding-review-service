from rest_framework import permissions


class IsCreatorOrCreateOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator_id == request.user.id
