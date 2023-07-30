from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BanViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'bans', BanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
