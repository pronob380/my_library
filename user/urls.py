from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard_view'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('user/', views.member_list_view, name='user_list'),
    path('create/', views.create_user, name='create_user'),
    path('user/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('user/update/<int:user_id>/', views.update_user_view, name='update_user'),
    path('update_user_status/<int:user_id>/', views.update_user_status, name='update_user_status'),
]
