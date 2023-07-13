from django.urls import path

from server.apps.posts.views import hello_world

urlpatterns = [
    path("", hello_world),
]