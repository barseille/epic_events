from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from EpicEvents import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'contrats', views.ContratViewSet)
router.register(r'events', views.EventViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/me/', views.UserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('api/', include(router.urls)),
    # path('sentry-test/', views.sentry_test, name='sentry_test'),
]
