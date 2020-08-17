from rest_framework import routers
from .api import UserViewSet
from .views import *

router = routers.DefaultRouter()
router.register('api/users', UserViewSet, basename='users')

urlpatterns = router.urls
