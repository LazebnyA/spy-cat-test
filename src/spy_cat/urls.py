from django.urls import path, include
from rest_framework.routers import DefaultRouter
from spy_cat.views import SpyCatViewSet, MissionViewSet, TargetViewSet

router = DefaultRouter()
router.register("spy-cats", SpyCatViewSet)
router.register("missions", MissionViewSet)
router.register("targets", TargetViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
