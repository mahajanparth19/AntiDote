from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login",views.login_view,name="login"),
    path("logout", views.logout_view, name="logout"),
    path("rform/<int:num>",views.rform,name="rform"),
    path("reg", views.reg, name="reg"),
    path("register", views.register, name="register"),
    path("registerD", views.register_Doctor, name="registerDoctor"),
    path("reports", views.showfile, name="reports"),
    path("View_Treatment",views.View_Treatment, name = "View_Treatment"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path("send/<int:nums>",views.send,name="send"),
    path("PTreat/<int:nums>",views.Patient_Treatment,name="PTreat"),
    path("NewTreat",views.view_new_treatments,name="NewTreat"),
    path("ActiveTreat",views.view_active_treatments,name="ActiveTreat"),
    path("DTreat/<int:nums>",views.Doctor_Treatment,name="DTreat"),
    path("Email_Forget",views.email_forgot,name="Email_Forget"),
    url(r'^Forgot/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.Forgot,name="Forgot")
]