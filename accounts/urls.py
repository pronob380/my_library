from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('youtube', views.youtube_search, name='youtube_search'),
    path('search/', views.search_wikipedia, name='search_wikipedia'),
]