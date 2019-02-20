from django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from json import dumps,load
from aimales import models as aimales_models
from django.forms.models import model_to_dict
import sys
import inspect
import json

# Create your views here.
@login_required
def aimalesIndex(request):
    return render(request, 'homepage.html')

@login_required
def nlpTagTools(request):
    datasets = {}
    for name, obj in inspect.getmembers(aimales_models, inspect.isclass):
        try:
            len(obj.objects.all())
            datasets[name] = obj
        except:
            print >> sys.stderr, "Table: %s doesn't exist." % name
    pcap_count = 2
    sample_count = 0
    all_records = None
    default_display_data = None
    if len(datasets):
        first_dataset = datasets.keys()[0]
        all_records = datasets[first_dataset].objects.all()
        if len(all_records):
            default_display_data = all_records[0].to_dict()
            all_records = all_records.values_list()
            sample_count = len(all_records)
        pcap_count = datasets[first_dataset].objects.values('pcap_md5').distinct().order_by('pcap_md5').count()
        default_display_data[u'word_segmentation_text'] = default_display_data[u'word_segmentation_text'].split(" ")
        print >> sys.stderr, default_display_data
    return_result = {
        'datasets': datasets.keys(), 
        'pcap_count': pcap_count,
        'sample_count': sample_count,
        'records': all_records,
        'display': default_display_data,
    }
    return render(request, 'nlp_tag_tools.html', return_result)

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
