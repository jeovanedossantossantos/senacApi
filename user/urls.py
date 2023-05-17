from django.urls import path

from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.urlpatterns import format_suffix_patterns
# https://github.com/rg3915/gallery/blob/master/gallery
urlpatterns = [
     path('token/', TokenObtainPairView.as_view() ),
     path('token/refresh/', TokenRefreshView.as_view()),
    
     # path('token/refresh/', TokenRefreshView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)