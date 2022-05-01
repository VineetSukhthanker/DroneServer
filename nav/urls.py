from .views import ThrottleView, ArmView
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('throttle/', ThrottleView.as_view()), # throttle API endpoint
    path('arm/', ArmView.as_view()), # Arm/disarm API endpoint
]


urlpatterns = format_suffix_patterns(urlpatterns)