from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("vote", views.vote, name="vote"),
    path("results", views.results, name="results"),
    # New Dashboard
    path("dashboard", views.dashboard, name="dashboard"),
]
