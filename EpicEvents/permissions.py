from rest_framework.permissions import BasePermission

class IsCommercial(BasePermission):
    message = "Vous n'avez pas la permission d'accéder à cette ressource. Seuls les utilisateurs avec le rôle 'Commercial' y ont accès."

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'COMMERCIAL')

class IsAdministration(BasePermission):
    message = "Vous n'avez pas la permission d'accéder à cette ressource. Seuls les utilisateurs avec le rôle 'Administration' y ont accès."

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'ADMINISTRATION')

class IsSupport(BasePermission):
    message = "Vous n'avez pas la permission d'accéder à cette ressource. Seuls les utilisateurs avec le rôle 'Support' y ont accès."

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'SUPPORT')
