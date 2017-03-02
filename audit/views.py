from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect

import django.utils.timezone

from django.contrib import auth

from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def index(request):
    return render(request,'index.html')


def login(request):
    """用户登录"""
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        # 前端模拟登录 检查后端能否正常接收数据
        # print("************************")
        # print(username,password)

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            try:
                if user.valid_begin_time and user.valid_end_time:
                    if django.utils.timezone.now() > user.valid_begin_time and django.utils.timezone.now()  < user.valid_end_time:
                        auth.login(request,user)
                        request.session.set_expiry(60*30)
                        return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/")
                    else:
                        return render(request,'login.html',{'login_err': 'User account is expired,please contact your IT guy for this!'})
                else:
                    auth.login(request, user)
                    request.session.set_expiry(60 * 30)
                    return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/")

            except ObjectDoesNotExist:
                    return render(request,'login.html',{'login_err': u'CrazyEye账户还未设定,请先登录后台管理界面创建CrazyEye账户!'})

        else:
            return render(request,'login.html',{'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'login.html')