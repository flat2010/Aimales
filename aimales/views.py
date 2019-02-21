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
import datetime

# resolve datetime can't be json serialized problem
class DateTimeJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

# Create your views here.
@login_required
def aimalesIndex(request):
    return render(request, 'homepage.html')

@login_required
@csrf_exempt
def fetchDataset(request, dataset, flag, flag_value, order_field="-id"):
    flag_value = 1 if u'1' == flag_value else 0
    datas = None
    result = {}
    try:
        data_class = getattr(aimales_models, dataset)
        if u'is_valid' == flag:
            datas = list(data_class.objects.filter(is_valid=flag_value).order_by(order_field).values())
        elif 'is_tagged' == flag:
            datas = list(data_class.objects.filter(is_tagged=flag_value).order_by(order_field).values())
        elif 'is_segmented' == flag:
            datas = list(data_class.objects.filter(is_segmented=flag_value).order_by(order_field).values())
    except:
        print >> sys.stderr, "Dataset: %s don't exist." % dataset
    return HttpResponse(json.dumps(datas, cls=DateTimeJsonEncoder))

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
        all_records = datasets[first_dataset].objects.all().order_by('-id')
        if len(all_records):
            default_display_data = all_records[0].to_dict()
            all_records = list(all_records.values())
            sample_count = len(all_records)
        pcap_count = datasets[first_dataset].objects.values('pcap_md5').distinct().order_by('pcap_md5').count()
        default_display_data[u'word_segmentation_text'] = default_display_data[u'word_segmentation_text'].split(" ")
    return_result = {
        'datasets': datasets.keys(), 
        'pcap_count': pcap_count,
        'sample_count': sample_count,
        'records': json.dumps(all_records, cls=DateTimeJsonEncoder),
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
