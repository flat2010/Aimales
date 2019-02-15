from django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from json import dumps,load

# Create your views here.
@login_required
def aimalesIndex(request):
    return render(request, 'index.html')

<<<<<<< HEAD
@login_required
def nlpTagTools(request):
    return render(request, 'nlp_tag_tools.html')

=======
>>>>>>> 82c87a3c131a95bcda66203a7f21262c5609a8bf
@csrf_exempt
def loginIndex(request):
    redirect_url = request.REQUEST.get('/aimales/login', '')
    if request.method == 'POST':
        uname = request.POST.get('username', '') 
        upwd = request.POST.get('password', '') 
        user = authenticate(username=uname, password=upwd)
        if user and user.is_active:
            login(request, user)
            return render(request, '/aimales/index.html')
    return render(request, "login.html")

@csrf_exempt
def loginValidate(request):
    result = {'Status': 'false'}
    if request.method == 'POST':
        uname = request.POST.get('username', '') 
        upwd = request.POST.get('password', '') 
        user = authenticate(username=uname, password=upwd)
        if user and user.is_active:
            login(request, user)
            result['Status'] = 'ok'
    return HttpResponse(dumps(result))
