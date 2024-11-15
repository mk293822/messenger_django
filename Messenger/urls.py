from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('message_room/<str:pk>/', views.message_room_view, name='message_room'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('request_friend_noti/', views.requested_friend_view, name='request_friend'),
    path('like_send/<str:pk>/', views.like_send, name='like_send'),
    path('image_send/<str:pk>/', views.image_send, name='image_send'),
]