from rest_framework.permissions import BasePermission


# Permission personnalisée pour les utilisateurs avec le rôle 'Commercial'
class IsCommercial(BasePermission):
    # Message d'erreur à afficher si la permission est refusée
    message = "Seuls les utilisateurs avec le rôle 'Commercial' y ont accès."

    # Méthode pour vérifier la permission
    def has_permission(self, request, view):
        # Retourne True si l'utilisateur est connecté et a le rôle 'Commercial'
        return bool(request.user and request.user.role == 'COMMERCIAL')


# Permission personnalisée pour les utilisateurs avec le rôle 'Administration'
class IsAdministration(BasePermission):
    message = "Seuls les utilisateurs avec le rôle 'Administration' y ont accès."

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'ADMINISTRATION')


# Permission personnalisée pour les utilisateurs avec le rôle 'Support'
class IsSupport(BasePermission):
    message = "Seuls les utilisateurs avec le rôle 'Support' y ont accès."

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'SUPPORT')
