from django.urls import path, include
from rest_framework import routers

from api.v3.award import AwardViewSet
from api.v3.badge import BadgeViewSet
from api.v3.user import UserViewSet
from api.v3.category import CategoryViewSet
from api.v3.course import CourseViewSet
from api.v3.userdata import UserDataViewSet
from api.v3.activitylog import ActivityLogViewSet

# Uncomment once ready to be deployed
router = routers.DefaultRouter()
# router.register(r'award', AwardViewSet)
# router.register(r'badge', BadgeViewSet)
# router.register(r'user', UserViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'course', CourseViewSet)
# router.register(r'userdata', UserDataViewSet)
# router.register(r'activitylog', ActivityLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
