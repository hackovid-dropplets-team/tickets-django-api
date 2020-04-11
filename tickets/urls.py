from django.urls import include, path, re_path
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'tickets', views.TicketsViewSet)
router.register(r'volunteering', views.VolunteeringViewSet)
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/',
            include('rest_auth.registration.urls')),
]
