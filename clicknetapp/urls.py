
from django.conf.urls import url
from django.urls import path
from .import views

urlpatterns = [
    path("",views.home,name="home"),
    # path("home/",views.home,name="home"),
    path("logout/",views.logout,name="logout"),
    path("profile/",views.profile,name = 'profile'),
    path("payout_rate/",views.payout_rate,name="payout_rate"),
    path("privacy_policy/",views.privacy,name="privacy"),
    path("terms/",views.terms,name="termsofus"),
    path("login/",views.log_in,name="login"),
    path("signup",views.signup,name="signup"),
    url(r'^activate/(?P<rendom>[0-9a-zA-Z]+)/(?P<uidb64>[0-9a-z]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path('resend_email/',views.resend_email,name='resend_email'),
    path("dashboard/",views.dashboard,name = "dashboard" ),
    path('account/',views.account,name = 'account'),
    path('shorturladmin/',views.shorturladmin,name='shorturladmin'),
    path('shorturl/',views.shorturl,name='shorturl'),
    path("myurls/",views.myurls,name="myurls"),
    path("createchart/",views.createchart,name="createchart"),
    path("geturl/",views.geturls,name="geturl"),
    path("refresh/",views.refresh,name="refresh"),
    path("refer/",views.refer,name="refer"),
    path("myteam/",views.myteam,name="myteam"),
    path("forgot_password/",views.forgot_password,name="forgot_password"),
    path("paymentstatus/",views.paymentstatus,name="paymentstatus"),
    path('redeem/',views.redeem,name = 'redeem'),
    path('adminarea/',views.adminarea,name = 'adminarea'),
    path('adminlogin/',views.adminlogin,name = 'adminlogin'),
    path('success/<int:id>/',views.redeemsuccess),
    path('block/<int:id>/',views.block),
    path('cancel/<int:id>/',views.redeemcancel),
    path('getip/',views.getip,name='getip'),
    path('contactmsg',views.contactmsg),
    path('getip/',views.getip),
    path('<str:code>/',views.get_url),
    
    path('forgot/password/<str:key>/',views.forgot_password_user),
    path('<int:id>/delete',views.delete),

]
