from django.shortcuts import render, redirect
from clicknetapp.models import *
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import auth
from django.conf import settings
from django.utils.crypto import get_random_string
from .tokens import account_activation_token
from django.contrib.auth import authenticate
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from urllib.parse import urlparse
from .import short_url as s
from django.utils import timezone
from datetime import timedelta
import decimal

# Create your views here.
def home(request):
    user = usertab.objects.all()
    link = userurltable.objects.all()
    allclick = 0
    for i in link:
        allclick = int(allclick) + int(i.click)
    alluser = user.count()
    alllink = link.count()
    d = {'alluser' : alluser,'alllink' : alllink,'allclick' : allclick}
    return render(request,"html/home/index.html",d)

def dashboard(request):
    if request.session.has_key('user_id'):
        clickearning = 0
        redeemsuccess = 0
        redeempanding = 0
        redeemcancel = 0
        totalclicks = 0
        obj = userurltable.objects.filter(user_id = request.session['user_id'])
        obj1 = balance.objects.get(user_id = request.session['user_id'])
        obj2 = redeemtable.objects.filter(user_id = request.session['user_id'])
        pastdate = timezone.now() - timedelta(days=9) + timedelta(minutes=330)
        nowdate = timezone.now() + timedelta(minutes=330)
        staticdata = statictab.objects.filter(date__range=[pastdate.date() , nowdate.date() ],user_id=request.session['user_id']).values()
        for data in obj:
            clickearning += decimal.Decimal(data.earning)
            totalclicks += int(data.click)
        if obj2 is not None:
            for dt in obj2:
                if dt.status == 0:
                    redeempanding += decimal.Decimal(dt.amount)
                elif dt.status == 1:
                    redeemsuccess += decimal.Decimal(dt.amount)
                else :
                    redeemcancel += decimal.Decimal(dt.amount)
        walletbalance = decimal.Decimal(obj1.blc)
        referblc = decimal.Decimal(obj1.referblc)
        totalredeem = redeemsuccess + redeempanding
        lifetimeearning = walletbalance + totalredeem
        notif = noti.objects.all()
        blc = balance.objects.get(user = request.session['user_id'])
        d1 = {"d" : notif,'blc' : blc.blc ,'totalclicks':totalclicks ,'lifetimeearning': lifetimeearning ,'totalredeem':totalredeem ,'redeemsuccess':redeemsuccess ,'redeempanding':redeempanding ,'clickearning':clickearning,'referblc':referblc,'staticdata' : list(staticdata)}
        return render(request,"html/dashboard.html",d1)
    else:
           return HttpResponseRedirect( settings.BASEURL + "login")
def payout_rate(request):
    return render(request,"html/home/payout-rate.html")
def privacy(request):
    return render(request,"html/home/privacy.html")
def terms(request):
    return render(request,"html/home/terms.html")
def log_in(request):
    if request.method == 'POST':
        uname = request.POST.get("uname")
        pwd = request.POST.get("password")
        try:
            obj = usertab.objects.get(username = uname , password = pwd)
        except:
            obj = None
        try:
            obj2 = usertab.objects.get(email = uname , password = pwd)
        except:
            obj2 = None
        if obj is not None:
            if obj.is_active == True:
                if obj.is_block == False:
                    request.session["user_id"] = obj.id
                    return HttpResponseRedirect("../dashboard")
                else:
                    d = {"error" : "Your Account Is Blocked By Click.Net Compney"}
                    return render(request,"html/home/login.html",d)
            else:
                d = {"error" : "Please verify your email address and login"}
                return render(request,"html/home/login.html",d)
        elif obj2 is not None:
            if obj2.is_active == True:
                request.session["user_id"] = obj2.id
                return HttpResponseRedirect("../dashboard")
            else:
                d = {"error" : "Please verify your email address and login"}
                return render(request,"html/home/login.html",d)
        else:
            d = {"error" : "Username and Password is invalid!"}
            return render(request,"html/home/login.html",d)
    else:
        return render(request,"html/home/login.html")
def signup(request):
    if request.method == 'POST':
        uname = request.POST.get("uname")
        email = request.POST.get("email")
        rcode = request.POST.get("refer")
        pwd = request.POST.get("password")
        rpwd = request.POST.get("re_password")
        obj1 = usertab.objects.filter(username = uname)
        obj2 = usertab.objects.filter(email = email)
        if rcode == "":
            rcode = None
        if obj1.count()>0 :
            dict_data1={'error1':'Username alrady exist please retry',"uname": uname,"email":email,"pwd":pwd,"rpwd":rpwd,'refercode':rcode}
            return render(request,"html/home/signup.html",dict_data1)
        elif obj2.count()>0 :
            dict_data2={'error2':'Email alrady exist please retry',"uname": uname,"email":email,"pwd":pwd,"rpwd":rpwd,'refercode':rcode}
            return render(request,"html/home/signup.html",dict_data2)
        elif pwd != rpwd :
            dict_data4={'error3':'Password does not match please retry',"uname": uname,"email":email,"pwd":pwd,"rpwd":rpwd,'refercode':rcode}
            return render(request,"html/home/signup.html",dict_data4)
        else:
            refer = usertab.objects.all()
            refercode = get_random_string(length=6, allowed_chars='ASDFGHJKLZXCVBNMQWERTYUIOP1234567890')
            j = 0
            while j==0:
                j+=1
                for i in refer:
                    if refercode == i.refercode:
                        refercode = get_random_string(length=6, allowed_chars='ASDFGHJKLZXCVBNMQWERTYUIOP1234567890')
                        j=0
                    else:
                        pass
            user = usertab(username = uname,email = email,password=pwd,is_active=False,referredby=rcode,refercode=refercode)
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('html/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': s.encode_url(user.id),
                'token': account_activation_token.make_token(user),
                'rendom': get_random_string(length=64, allowed_chars='qwertyuiopasdfghjklzxcvbnmASDFGHJKLZXCVBNMQWERTYUIOP1234567890')
            })
            mail_subject = 'Activate your account.'
            send_mail(mail_subject, "", "hp30405@gmail.com", [email] ,fail_silently=False,html_message=message )
            ub = balance(user = user,blc= 500)
            ub.save()
            return render(request,'html/done.html')
    else:
        data = []
        for i in usertab.objects.all():
            data.append(i)
        d = {"refer" : data}
        return render(request,"html/home/signup.html",d)

def resend_email(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        try:
            user = usertab.objects.get(email = email)
        except:
            user = None
        if user is not None:
            if user.is_active == False:
                current_site = get_current_site(request)
                message = render_to_string('html/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': s.encode_url(user.id),
                    'token':account_activation_token.make_token(user),
                    'rendom': get_random_string(length=64, allowed_chars='qwertyuiopasdfghjklzxcvbnmASDFGHJKLZXCVBNMQWERTYUIOP1234567890')
                })
                mail_subject = 'Activate your account.'
                send_mail(mail_subject, "", "hp30405@gmail.com", [email], fail_silently=True ,html_message=message )
                return render(request,'html/done.html')
            else:
                d = {"error" : "you are alrady confirm your email please login","email":email}
                return render(request,"html/resendemail.html",d)
        else:
            d = {"error" : "this email is not registerd please sign up Or something went wrong","email":email}
            return render(request,'html/resendemail.html',d)
    else:
        return render(request,"html/resendemail.html")

def activate(request,rendom, uidb64, token):
    try:
        uid = s.decode_url(uidb64)
        user = usertab.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist ):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "html/emailconfirmed.html", {"user" : user} )

    else:
        return render(request, "html/emailconfirmed.1.html")
def logout(request):
    auth.logout(request)
    return redirect('login')
def profile(request):
    if request.session.has_key('user_id'):
        blc = balance.objects.get(user = request.session['user_id'])
        obj = usertab.objects.get(id = request.session['user_id'] )
        notif = noti.objects.all()
        users = usertab.objects.all()

        for i in users:
            if i.refercode == obj.referredby:
                referuser = i.username
                break
            else:
                referuser = None
        d = {"d" : notif,'blc' : blc.blc,"user" : obj,'referuser':referuser }
        return render(request,'html/profile.html',d)
    else:
        return HttpResponseRedirect( settings.BASEURL + "login")


def account(request):
    if request.session.has_key('user_id'):
        blc = balance.objects.get(user = request.session['user_id'])
        obj = usertab.objects.get(id = request.session['user_id'] )
        notif = noti.objects.all()
        data = payment.objects.all()
        d = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data}
        if request.method == 'POST' and request.FILES['profileimg']:
            valid = useraddress.objects.filter(user = request.session['user_id'] )
            if valid.count() == 0:
                name = request.POST.get('name')
                adr = request.POST.get('adr')
                state = request.POST.get('state')
                zip = request.POST.get('zip')
                phone = request.POST.get('phone')
                img = request.FILES['profileimg']
                obj = useraddress(name = name,adr = adr,state = state,zip = zip,phone = phone,user_id = request.session['user_id'] )
                obj.save()
                obj2 = usertab.objects.get(id = request.session['user_id'] )
                obj2.img = img
                obj2.save()
                d2 = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data,'success' : "You'r address is saved successfully"}
                return render(request,'html/form.html',d2)
            else:
                d3 = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data,'error' : 'You are saved your address once'}
                return render(request,'html/form.html',d3)
        else:
            return render(request,'html/form.html',d)
    else:
        return HttpResponseRedirect( settings.BASEURL + "login")
def get_url(request,code):
    for record in iptable.objects.all():
        exp = record.created_date + timedelta(minutes=1)
        if exp <= timezone.now():
            record.delete()
    valid = codetable.objects.filter(code = code)
    if valid.count() > 0 :
        key = s.decode_url(code)
        obj = userurltable.objects.get(id=key)
        d = {"data":obj}
        return render(request,"html/geturl.html",d)
    else:
        return render(request,'html/pagenotfound.html')

def contactmsg(request):
    return HttpResponseRedirect('../')


def redeem(request):
    if request.session.has_key('user_id'):
        redeemsuccess = 0
        redeempanding = 0
        obj2 = redeemtable.objects.filter(user_id = request.session['user_id'])
        for dt in obj2:
            if dt.status == 0:
                redeempanding += decimal.Decimal(dt.amount)
            elif dt.status == 1:
                redeemsuccess += decimal.Decimal(dt.amount)
        blc = balance.objects.get(user = request.session['user_id'])
        obj = usertab.objects.get(id = request.session['user_id'] )
        notif = noti.objects.all()
        data = payment.objects.all()
        d = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data , "redeempanding" : redeempanding , "redeemsuccess" : redeemsuccess }
        if request.method == 'POST' :
            paymentm = request.POST.get("payment")
            paddress = request.POST.get("paddress")
            amount = request.POST.get("amount")
            try:
                ifsc = request.POST.get("ifsc")
            except:
                ifsc = None
            
            obj1 = usertab.objects.filter(id = request.session['user_id'])
            if obj1.count() > 0 :
                if blc.blc >= int(amount) :
                    if int(amount) >= 100 :
                        valid = useraddress.objects.filter(user = request.session['user_id'] )
                        if valid.count() > 0 :
                            if paddress is None:
                                d4 = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data, "error" : 'Please Add Your Payment Address' }
                                return render(request,'html/redeem.html',d4)
                            else:
                                blc.blc = blc.blc - int(amount)
                                blc.save()
                                if ifsc is None:
                                    rdm = redeemtable(user = obj,paymentmode_id = paymentm,paddress = paddress,amount = amount)
                                    rdm.save()
                                else:
                                    rdm = redeemtable(user = obj,paymentmode_id = paymentm,paddress = paddress,amount = amount,ifsc = ifsc)
                                    rdm.save()
                                d4 = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data, "success" : 'Your Redeem Is Success You Will Get Amount In 24 Hour Thank You.' }
                                # return render(request,'html/redeem.html',d4)
                                return HttpResponseRedirect(settings.BASEURL + "paymentstatus")
                        else :
                            d4 = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data, "error" : 'First Add Your Billing Address In Your Account Setting' }
                            return render(request,'html/redeem.html',d4)
                    else:
                        d3 = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data, "error" : 'Minimum redeem is 100Rs.' }
                        return render(request,'html/redeem.html',d3)
                else:
                    d1 = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data, "error" : 'Not enough balance for redeem' }
                    return render(request,'html/redeem.html',d1)
            else:
                d2 = {"d" : notif,'blc' : blc.blc,"user" : obj ,'data' : data, "error" : 'User is not verifyed' }
                return render(request,'html/redeem.html',d2)
        else:
            return render(request,'html/redeem.html',d)
    else:
        return HttpResponseRedirect( settings.BASEURL + "login")

def delete(request,id):
    if request.session.has_key('user_id'):
        valid = userurltable.objects.filter(user_id = request.session['user_id'])
        if valid.count() > 0:
            obj = userurltable.objects.get(id = id)
            obj.delete()
            return HttpResponseRedirect(settings.BASEURL+'myurls')
        else:
            return HttpResponse('you are not eligiable for delete this url')
    else:
        return HttpResponseRedirect( settings.BASEURL + "login")


def myurls(request):
    if request.session.has_key('user_id'):
        notif = noti.objects.all()
        blc = balance.objects.get(user = request.session['user_id'])
        d1 = {"d" : notif,'blc' : blc.blc }
        return render(request,'html/myurls.html',d1)
    else:
        return HttpResponseRedirect( settings.BASEURL + "login")


def getip(request):
    if request.method == 'POST' :
        ip = request.POST.get('ip')
        url = request.POST.get('url')
        obj = iptable.objects.filter(ip = ip)
        if obj.count() > 0 :
            return HttpResponse("nc")
        else:
            obj1 = userurltable.objects.get(url = url)
            obj1.click = int(obj1.click) + int(1)
            obj1.earning = decimal.Decimal(obj1.earning) + decimal.Decimal(0.1)
            obj1.save()
            inddate = timezone.now() + timedelta(minutes = 330)
            if obj1.user is not None:
                try:
                    check = statictab.objects.get(user = obj1.user,date = inddate.date() )
                except:
                    check = None
                if check is not None:
                    if check.date == inddate.date():
                        check.click =  int(check.click) + int(1)
                        check.save()
                    else:
                        static = statictab(user = obj1.user,click = 1)
                        static.save()
                else:
                    static = statictab(user = obj1.user,click = 1)
                    static.save()
            try:
                obj2 = balance.objects.get(user_id = obj1.user_id)
                obj2.blc = decimal.Decimal(obj2.blc) + decimal.Decimal(0.1)
                obj2.referbyblc = decimal.Decimal(obj2.referbyblc) + decimal.Decimal(0.02)
                obj2.save()
                obj3 = usertab.objects.get(id = obj2.user_id)
                obj4 = usertab.objects.get(refercode = obj3.referredby)
                obj5 = balance.objects.get(user_id = obj4.id)
                obj5.blc = decimal.Decimal(obj5.blc) + decimal.Decimal(0.02)
                obj5.referblc = decimal.Decimal(obj5.referblc) + decimal.Decimal(0.02)
                obj5.save()
            except:
                obj2 = None
            obj3 = iptable(ip = ip )
            obj3.save()
            return HttpResponse("c")


def shorturladmin(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        spliturl = urlparse(url)
        url_domain = spliturl.netloc
        obj1 = userurltable.objects.filter(url = url)
        d = {"urlerror" : "we are not short this domain url's","url":url}
        if url_domain == "click2earn.net":
            return JsonResponse(d)
        elif url_domain == settings.BASEDOMAIN:
            return JsonResponse(d)
        elif url_domain == "bit.ly":
            return JsonResponse(d)
        elif url_domain == "clnk.in":
            return JsonResponse(d)
        elif url_domain == "amazon.to":
            return JsonResponse(d)
        elif url_domain == "goo.gl":
            return JsonResponse(d)
        elif url_domain == "za.gl":
            return JsonResponse(d)
        else :
            if obj1.count()>0:
                obj2 = userurltable.objects.get(url = url)
                code = s.encode_url(obj2.id)
                shortened_url = settings.BASEURL + code
                d = {"url": shortened_url , 'error' : 'this url alrady shorted' , 'error1' : 'ok' }
                return JsonResponse(d)
            else:
                obj4 = userurltable(url = url,user_id = request.session['user_id'])
                obj4.save()
                obj5 = userurltable.objects.get(url = url)
                url_id = obj5.id
                code = s.encode_url(url_id)
                ok = codetable(code = code)
                ok.save()
                shortened_url = settings.BASEURL + code
                obj4.shorturl = shortened_url
                obj4.save()
                d = {"url": shortened_url, 'success' : 'your url short success' , 'error1' : 'ok2', 'error2' : 'ok2' }
                return JsonResponse(d)
def shorturl(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        spliturl = urlparse(url)
        url_domain = spliturl.netloc
        obj1 = userurltable.objects.filter(url = url)
        if url_domain == "click2earn.net":
            d = {"urlerror" : "we are not short this domain url's","url":url}
            return JsonResponse(d)
        elif url_domain == settings.BASEDOMAIN:
            d = {"urlerror" : "we are not short this domain url's","url":url}
            return JsonResponse(d)
        elif url_domain == "bit.ly":
            d = {"urlerror" : "we are not short this domain url's","url":url}
            return JsonResponse(d)
        elif url_domain == "clnk.in":
            d = {"urlerror" : "we are not short this domain url's","url":url}
            return JsonResponse(d)
        elif url_domain == "amazon.to":
            d = {"urlerror" : "we are not short this domain url's","url":url}
            return JsonResponse(d)
        elif url_domain == "goo.gl":
            d = {"urlerror" : "we are not short this domain url's","url":url}
            return JsonResponse(d)
        elif url_domain == "za.gl":
            d = {"urlerror" : "we are not short this domain url's","url":url}
            return JsonResponse(d)
        else :
            if obj1.count()>0:
                obj2 = userurltable.objects.get(url = url)
                code = s.encode_url(obj2.id)
                shortened_url = settings.BASEURL + code
                d = {"url": shortened_url , 'error' : 'this url alrady shorted' , 'error1' : 'ok'}
                return JsonResponse(d)
            else:
                obj4 = userurltable(url =  url )
                obj4.save()
                obj5 = userurltable.objects.get(url = url)
                url_id = obj5.id
                code = s.encode_url(url_id)
                obj6 = codetable(code = code)
                obj6.save()
                shortened_url = settings.BASEURL + code
                d = {"url": shortened_url , 'success' : 'your url short success' , 'error1' : 'ok2', 'error2' : 'ok2'}
                return JsonResponse(d)


def paymentstatus(request):
    if request.session.has_key('user_id'):
        notif = noti.objects.all()
        blc = balance.objects.get(user = request.session['user_id'])
        try:
            userurls = userurltable.objects.filter(user_id = request.session['user_id'])
        except:
            userurls = None
        payments = redeemtable.objects.filter(user_id = request.session['user_id'] ).prefetch_related("paymentmode")
        d1 = {"d" : notif,'blc' : blc.blc ,'userurls' : userurls,"payments" : payments}
        return render(request,'html/paymentstatus.html',d1)
    else:
        return HttpResponseRedirect( settings.BASEURL + "login")
def adminlogin(request):
    try:
        if request.method == 'POST':
            uname = request.POST.get("uname")
            pwd = request.POST.get("password")
            obj = usertab.objects.get(username = uname , password = pwd)
            if obj.is_superuser == True:
                request.session["adminuser_id"] = obj.id
                return HttpResponseRedirect(settings.BASEURL + 'adminarea')
            else:
                return render(request,'html/pagenotfound.html')
        else :
            return render(request,'html/home/login.html')
    except:
        return render(request,'html/pagenotfound.html')

def redeemsuccess(request,id):
    user = redeemtable.objects.get(id = id)
    user.status += 1
    user.save()
    return HttpResponseRedirect("http://127.0.0.1:8000/adminarea")
def redeemcancel(request,id):
    user = redeemtable.objects.get(id = id)
    user.status += 2
    user.save()
    blc = balance.objects.get(user = user.user)
    blc.blc += int(user.amount)
    blc.save()
    return HttpResponseRedirect("http://127.0.0.1:8000/adminarea")
    
def myteam(request):
    if request.session.has_key('user_id'):
        notif = noti.objects.all()
        blc = balance.objects.get(user = request.session['user_id'])
        user = usertab.objects.get(id = request.session['user_id'])
        team = usertab.objects.filter(referredby = user.refercode)
        # referbyblc = balance.objects.filter(user = team)
        d = {"d" : notif,'blc' : blc.blc ,'team' : team}
        return render(request,"html/myteam.html",d)
    else:
        return HttpResponseRedirect( settings.BASEURL + "login")

def refer(request):
    if request.session.has_key('user_id'):
        notif = noti.objects.all()
        blc = balance.objects.get(user = request.session['user_id'])
        obj = usertab.objects.get(id = request.session['user_id'] )
        user = usertab.objects.get(id = request.session['user_id'])
        team = usertab.objects.filter(referredby = user.refercode)
        totalrefer = team.count()
        d = {"d" : notif,'blc' : blc.blc,'user':obj,"totalrefer":totalrefer}
        return render(request,"html/refer.html",d)
    else:
        return HttpResponseRedirect( settings.BASEURL + "login")




def refresh(request):
    pastdate = timezone.now() - timedelta(days=9) + timedelta(minutes=330)
    nowdate = timezone.now() + timedelta(minutes=330)
    staticdata = statictab.objects.filter(date__range=[pastdate.date() , nowdate.date() ],user_id=request.session['user_id'])
    d = []
    for data in staticdata:
        d.append(data.date)
    return HttpResponse(d)


def geturls(request):
    if request.session.has_key('user_id'):
        userurls = userurltable.objects.filter(user_id = request.session['user_id']).values()
        d={"data" : list(userurls)}
        return JsonResponse(d)
    else:
        pass
def createchart(request):
    if request.session.has_key('user_id'):
        pastdate = timezone.now() - timedelta(days=10) + timedelta(minutes=330)
        nowdate = timezone.now() + timedelta(minutes=330)
        staticdata = statictab.objects.filter(date__range=[pastdate.date() , nowdate.date() ],user_id=request.session['user_id'])
        datedata = []
        clickdata = []
        for i in staticdata:
            datedata.append(i.date)
            clickdata.append(i.click)
        if len(datedata) == 0:
            datedata.append(timezone.now().date())
            clickdata.append(0)        
        d={"datedata" : datedata,"clickdata":clickdata}
        return JsonResponse(d)
    else:
        pass

def adminarea(request):
    try:
        if request.session.has_key('adminuser_id'):
            obj = usertab.objects.get(id = request.session['adminuser_id'])
            if obj.is_superuser == True:
                data = redeemtable.objects.filter(status = 0)
                alluser = usertab.objects.all()
                d = {"data" : data,'alluser' : alluser}
                return render(request,'html/adminarea.html',d)
            else:
                return render(request,'html/pagenotfound.html')
        else:
            return render(request,'html/pagenotfound.html')
    except:
        return render(request,'html/pagenotfound.html')

def block(request,id):
    user = usertab.objects.get(id = id)
    user.is_block = True
    user.save()
    return HttpResponseRedirect("http://127.0.0.1:8000/adminarea")
        

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            obj = usertab.objects.get(email = email)
        except:
            obj = None
        if obj is not None:
            key = get_random_string(length=64, allowed_chars='ASDFGHJKLZXCVBNMQWERTYUIOP1234567890qwertyuioplkjhgfdsazxcvbnm')
            obj1 = password_change(user = obj ,key = key)
            obj1.save()
            current_site = get_current_site(request)
            message = render_to_string('html/password_reset_email.html', {
                'user': obj,
                'domain': current_site.domain,
                'rendom': key
            })
            mail_subject = 'Password Resate'
            send_mail(mail_subject, "", "hp30405@gmail.com", [email], fail_silently=True ,html_message=message )
            return render(request,'html/password_emaildoen.html')
        else:
            d = {'error':'Email Is Invalid Please Enter a Valid Email'}
            return render(request,'html/forgot_password.html',d)
    else:
        return render(request,'html/forgot_password.html')

def forgot_password_user(request,key):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        if pwd1 == pwd2:
            user = usertab.objects.get(id = user_id)
            user.password = pwd1
            user.save()
            obj = password_change.objects.get(key = key)
            obj.delete()
            return render(request,'html/password_changed.html')
        else:
            d = {'error':'Password And Confirm Password Does Not Match','user_id' : user_id}
            return render(request,'html/passwordchange.html',d)
    else:
        try:
            user = password_change.objects.get(key = key)
        except:
            user = None
        if user is not None:
            d = { 'user_id' : user.user_id }
            return render(request,'html/passwordchange.html',d)
        else:
            return render(request,'html/pagenotfound.html')


