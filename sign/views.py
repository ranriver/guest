from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#导入,可以使此次请求忽略csrf校验
from django.views.decorators.csrf import csrf_exempt
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#在处理函数加此装饰器即可
@csrf_exempt
def post(request):
     name=request.post['name']
     return HttpResponse('welcome!{}'.format(name))

# Create your views here.
def index(request):
    #return HttpResponse("Hello Django!")
    return render(request, "index.html")

# login opration
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        #if username == 'admin' and password == 'admin123':
        if user is not None:
            auth.login(request, user)# login
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            request.session['user'] = username  # save the session to browser
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})

# 发布会管理
@login_required
def event_manage(request):
    # username = request.session.get('user', '') # read the browser's session
    # return render(request, "event_manage.html", {"user":username})
    event_list = Event.objects.all().order_by('id')
    username = request.session.get('user', '')
    paginator = Paginator(event_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "event_manage.html", {"user": username, "events": contacts})

# 发布会名称搜索
@login_required
def event_search_name(requtest):
    username = requtest.session.get('user', '')
    event_search_name = requtest.GET.get("name", "")
    event_list = Event.objects.filter(name_contanis=event_search_name).order_by('id')
    paginator = Paginator(event_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(requtest, "event_manage.html", {"user": username, "events":contacts})

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all().order_by('id')
    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    # return render(request, "guest_manage.html", {"user": username, "guests": guest_list})
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

# 嘉宾搜索
@login_required
def guest_search_name(requtest):
    username = requtest.session.get('user', '')
    guest_search_name = requtest.GET.get("name", "")
    event_list = Event.objects.filter(name_contanis=guest_search_name).order_by('id')
    paginator = Paginator(event_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    # return render(requtest, "event_manage.html", {"user": username, "events":event_list})
    return render(requtest, "event_manage.html", {"user": username, "guests":contacts})


# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


# 签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success!', 'guest': result})


# 退出登录
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response