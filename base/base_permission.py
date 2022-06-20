from rest_framework.permissions import BasePermissionMetaclass


class BasePermissionTest(metaclass=BasePermissionMetaclass):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.

        """
        print("in step has permission")
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        print("in step has obj permission ")
        return True

