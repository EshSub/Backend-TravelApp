from django.urls import path, include
from cms.viewsets.UserViewset import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"register", UserViewSet)

urlpatterns = router.urls