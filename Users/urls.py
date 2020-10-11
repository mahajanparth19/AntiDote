from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login",views.login_view,name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("registerD", views.register_Doctor, name="registerDoctor"),
    path("reports", views.showfile, name="reports"),
    path("View_Treatment",views.View_Treatment, name = "View_Treatment"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path('SendToDoc', views.SendToDoc.as_view(), name='SendToDoc'),

]