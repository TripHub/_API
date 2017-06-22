"""triphub_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from apps.user.views import UserViewSet
from apps.trip.views import TripViewSet
from apps.destination.views import DestinationViewSet
from apps.invite.views import InviteViewSet, InvitePublicViewSet


router = routers.SimpleRouter()
router.register(r'user', UserViewSet, base_name='user')
router.register(r'trip', TripViewSet, base_name='trip')
router.register(r'destination', DestinationViewSet, base_name='destination')
router.register(r'invite', InviteViewSet, base_name='invite')
router.register(r'invite', InvitePublicViewSet, base_name='invite')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
