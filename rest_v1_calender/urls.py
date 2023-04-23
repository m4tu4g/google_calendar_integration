from django.urls import path

from .views import GoogleCalendarRedirectView, GoogleCalendarInitView, GoogleCalenderHelloWorldView


urlpatterns = [
    path('init/', GoogleCalendarInitView, name='calender_init'),
    path('redirect/', GoogleCalendarRedirectView, name='calender_redirect'),
    path('hello/', GoogleCalenderHelloWorldView, name='calender_hello_world'),
]