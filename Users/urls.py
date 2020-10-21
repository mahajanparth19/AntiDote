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
    path("NewTreat",views.view_new_treatments,name="NewTreat"),
    path("ActiveTreat",views.view_active_treatments,name="ActiveTreat"),
    path("Treat/<int:nums>",views.Treats,name="Treat"),
    path("Email_Forget",views.email_forgot,name="Email_Forget"),
    url(r'^Forgot/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.Forgot,name="Forgot"),
    path("Edit_profile",views.Edit_profile,name="Edit_profile"),
    path("Change_Password",views.Change_Password,name="Change_Password"),
    path("delete_Treatment/<int:nums>",views.delete_Treat,name="Delete_Treatment"),
    path("Complete_Treatment/<int:nums>",views.Complete_Treat,name="Complete_Treatment"),
    path("not_new/<int:nums>",views.not_new,name="not_new"),
]