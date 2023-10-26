from django.urls import path
from . import views

# UrlConf
urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('register/', views.registerPage, name='register'),

    path("", views.home, name="home"),
    path("list/<str:pk>", views.list, name="list"),
    path("profile/<str:pk>", views.userProfile, name="user-profile"),

    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<int:pk>/", views.updateRoom, name="update-room"),
    path("delete-room/<int:pk>/", views.deleteRoom, name="delete-room"),

    path("delete-message/<int:pk>/", views.deletemessage, name="delete-message"),   
]
