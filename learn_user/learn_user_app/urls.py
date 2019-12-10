from django.urls import path
from learn_user_app import views
app_name = "learn_user_app"
urlpatterns = [
    path('register/',views.register),
    path('login/',views.login_user,name="login_user")
]
