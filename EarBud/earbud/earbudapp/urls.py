from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("adddata/", views.editData, name = "adddata"),
    path("showplaylist/", views.viewPlaylist, name="showplaylist"),
    path("generatereport/", views.generateReport, name="generatereport")]