
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("predict/", views.predict_view, name="predict"),
    path("history/", views.history, name="history"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("train/", views.train_view, name="train"),
]