from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AuthView

router = DefaultRouter()
router.register(r'auth', AuthView, basename='auth')

urlpatterns = router.urls

urlpatterns += []
