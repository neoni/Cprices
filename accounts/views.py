# -*- coding:UTF-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from accounts.models import ClientId


def home(request):
    return render_to_response('home.html',{'user':request.user})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('name', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            request.session.set_expiry(30*60)
            return HttpResponseRedirect("/", RequestContext(request))
        else:
            errors = u"账户不存在或密码错误"
            return render_to_response("login.html",{'errors':errors},RequestContext(request))
    else:
        return render_to_response('login.html',RequestContext(request))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def register(request):
    if request.method == 'POST':
        errors = {}
        email = request.POST.get('email', '')
        username = request.POST.get('name', '')
        password = request.POST.get('password', '')
        user =  User.objects.filter(email=email)
        if len(user) > 0:
            errors['emailerrors'] = "此邮箱已注册过"
        user =  User.objects.filter(username=username)
        if len(user) > 0:
            errors['nameerrors'] = "此用户名已存在"
        if errors:
            return render_to_response('register.html', errors, RequestContext(request))
        user = User.objects.create_user(username, email, password)
        user.save()
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session.set_expiry(30*60)
        return HttpResponseRedirect("/", RequestContext(request))
    else:
        return render_to_response('register.html', RequestContext(request))


def forgotpasswd(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        try:
            user =  User.objects.get(email=email)
            try:
                password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789');
                user.set_password(password)
                user.save()
                title='Cprices 忘记密码服务'
                message=u"您好!\n您的新密码是" + password + \
                u"。您可以登录后进行密码修改。下次不要忘记了~\n谢谢您对Cprices的支持!\n\n\n\nCprices开发负责人"
                sender='cprices@163.com'
                mail_list=[email,]
                send_mail(
                            subject=title,
                            message=message,
                            from_email=sender,
                            recipient_list=mail_list,
                            fail_silently=False,
                            connection=None
                        )
            except Exception:
                pwdmailerrors = u"发送邮件失败,请检查邮箱是否正确"
                return render_to_response('forgotpasswd.html', {'pwdmailerrors':pwdmailerrors}, RequestContext(request))
            info = u"已发送新密码到邮箱，去查收吧"
            return render_to_response('forgotpasswd.html', {'info':info}, RequestContext(request))
        except User.DoesNotExist:
            pwdmailerrors = "该邮箱并不是注册用户"
            return render_to_response('forgotpasswd.html',{'pwdmailerrors':pwdmailerrors},RequestContext(request))
    else:
        return render_to_response('forgotpasswd.html',RequestContext(request))


def changepasswd(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            oldpwd = request.POST.get('oldpwd', '')
            newpwd = request.POST.get('newpwd', '')
            if request.user.check_password(oldpwd):
                request.user.set_password(newpwd)
                request.user.save()
                info = u'密码修改成功'
                return render_to_response('changepwd.html',{'info':info,'user':request.user},RequestContext(request))
            else:
                info = u'旧密码错误'
                return render_to_response('changepwd.html',{'info':info,'user':request.user},RequestContext(request))
        else:
            return render_to_response('changepwd.html',RequestContext(request))
    else:
        return HttpResponseRedirect("/login")


def verify(request,username,password,cid):
    user = auth.authenticate(username=username, password=password)
    if len(cid) != 32:
        return HttpResponse('ERROR')
    if user is not None and user.is_active:
        try:
            client = ClientId.objects.get(cid=cid,user=user)
        except ClientId.DoesNotExist:
            client = ClientId(cid=cid,user=user)
            client.save()
        return HttpResponse('SUCCESS')
    else:
        return HttpResponse('ERROR')


def logoff(request,cid):
    try:
        client = ClientId.objects.get(cid=cid)
        client.delete()
        return HttpResponse('SUCCESS')
    except ClientId.DoesNotExist:
        return HttpResponse('None')
