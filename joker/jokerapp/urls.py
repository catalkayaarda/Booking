from django.urls import path , include
from jokerapp import views
from jokerapp.views import  RoomListApi


urlpatterns = [
    path('api/availablerooms', views.AvailableRoomsApi, name='availablerooms-list-create'),
    path('api/register', views.UserRegister.as_view(), name='register'),
    path("api/login", views.UserLogin.as_view(), name="login"),
    path('api/logout', views.UserLogout.as_view(), name='logout'),
    path('api/user', views.UserView.as_view(), name='user'),
    path('api/listrooms', views.RoomApi),
    path('api/bookroom', views.BookApi, name='booking'),
    path('api/rooms/', RoomListApi.as_view(), name='room_list'),
    path('api/rooms/<int:pk>/', views.Delete.as_view(), name='delete-room'),

]
