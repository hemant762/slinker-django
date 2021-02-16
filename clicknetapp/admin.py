from django.contrib import admin
from clicknetapp.models import noti,balance,payment,userurltable,redeemtable,useraddress,usertab
# Register your models here.
admin.site.register(noti)
admin.site.register(payment)
admin.site.register(balance)
admin.site.register(userurltable)
admin.site.register(redeemtable)
admin.site.register(useraddress)
admin.site.register(usertab)
