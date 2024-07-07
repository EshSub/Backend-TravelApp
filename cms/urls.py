from django.urls import path, include
from cms.viewsets.UserViewset import UserViewSet
from rest_framework import routers
from cms.views import ProfileViewSet, EmailConfirmationViewSet, DistrictViewSet, ProvinceViewSet, PlaceViewSet, ActivityViewSet, PlaceActivityViewSet, TypeViewSet, TagViewSet

router = routers.DefaultRouter()

router.register(r"user", UserViewSet)
router.register(r"profile", ProfileViewSet)
router.register(r"emailconfirmation", EmailConfirmationViewSet)
router.register(r"district", DistrictViewSet)
router.register(r"province", ProvinceViewSet)
router.register(r"place", PlaceViewSet)
router.register(r"activity", ActivityViewSet)
router.register(r"placeactivity", PlaceActivityViewSet)
router.register(r"type", TypeViewSet)
router.register(r"tag", TagViewSet)


urlpatterns = router.urls