from django.urls import path

from .views import GoogleCalendarInitView, GoogleCalendarRedirectView


urlpatterns = [
    path('init/', GoogleCalendarInitView),
    path('redirect/', GoogleCalendarRedirectView),
]