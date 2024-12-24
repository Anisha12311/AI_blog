from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path('login', views.user_login),
    path('signup', views.signup),
    path('logout', views.user_logout),
    path('generate_blog', views.generate_blog)
]

