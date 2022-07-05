"""gamelist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

""" This will allow me to call the view() functions from views.py (source: 
https://www.youtube.com/watch?v=pRNhdI9PVmg&list=PLH9Qw2PrioB4_n5Z4nLCQGp82zxl5R7Pq&index=2&t=704s )
"""
from . import views

""" The 'index' path will be the home page.

Turns out that, if I want my users to log out, I also need to add a log out link here in urls.py.

I will add <str:variable> so that, if I send the user to "/game_uuid/edit", I will be able to edit the specific
game that I want to edit without displaying "1" o "3" in the URL. 
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.login_user, name='login_user'),
    path("logout/", views.logout_user, name="logout_user"),
    path("add/", views.add_game, name="add_game"),
    path("<str:game_uuid>/edit/", views.edit, name="edit"),
    path("<str:game_uuid>/delete/", views.delete, name="delete"),
]
