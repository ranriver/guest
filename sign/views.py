from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#导入,可以使此次请求忽略csrf校验
from django.views.decorators.csrf import csrf_exempt
from sign.models import Event, Guest
 
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
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, "event_manage.html", {"user": username, "events": event_list})

# 发布会名称搜索
@login_required
def event_search_name(requtest):
    username = requtest.session.get('user', '')
    event_search_name = requtest.GET.get("name", "")
    event_list = Event.objects.filter(name_contanis=event_search_name)
    return render(requtest, "event_manage.html", {"user": username, "events":event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})

# 嘉宾搜索
@login_required
def guest_search_name(requtest):
    username = requtest.session.get('user', '')
    guest_search_name = requtest.GET.get("name", "")
    event_list = Event.objects.filter(name_contanis=guest_search_name)
    return render(requtest, "event_manage.html", {"user": username, "events":event_list})