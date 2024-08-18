from django.urls import include, path
from rest_framework import routers

from products.views import ProductViewSet, UniqueProductViewSet

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"unique-products", UniqueProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),

]