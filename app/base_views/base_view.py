from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
import json

from app.processLogic.EasyDataProcessor import *
import logging
import os

easyDataProcessor = EasyProccessor()

def f_index(request):
    return render(request, 'base_data_manage.html')
    #return render(request, 'test.html')


@csrf_exempt
def pre_process_data(request):

    process_data_path = request.GET['path']
    easyDataProcessor.pre_process_xls_data(process_data_path)
    json_response_data = {'code': 1, 'msg': process_data_path}

    return HttpResponse(json.dumps(json_response_data))


def data_load(request):

    data_src = request.GET['datasource']
    path = request.GET['path']
    if data_src is None or len(data_src) == 0:
        json_reponse_data = {'code': 0, 'msg': '实验数据源为空'}
    if path is None or len(path) == 0:
        json_reponse_data = {'code': 0, 'msg': 'internal error'}

    dataitems = easyDataProcessor.load_data(path)

    json_response_data = {'code':1, 'msg': 'load success', 'data':
        {
            'count': len(dataitems),
            'items': dataitems
        }}
    return HttpResponse(json.dumps(json_response_data))


def load_real_x(request):
    x_path = request.GET['xpath']
    if x_path is None or len(x_path) == 0:
        json_response_data = {'code': 0, 'msg': '未导入真实浓度文件'}
    else:
        dataitems = easyDataProcessor.load_xreal_value(x_path)
        if dataitems is None:
            json_response_data = {'code': 0, 'msg': '浓度值为空,或者浓度条数与实验数据条数不符合'}
        else:
            json_response_data = {'code': 1, 'msg': '导入x真实浓度成功', 'data': {
                'count': len(dataitems),
                'items': dataitems
            }}
    return HttpResponse(json.dumps(json_response_data))


def curve_fit(request):
    is_select_all = json.loads(request.GET['isall'])
    curve_result = easyDataProcessor.curve_fit(is_select_all)
    if os.path.exists(curve_result):
        json_response_data = {'code': 1, 'msg': '拟合成功', 'data':{
            'curveimage': curve_result
        }}
    else:
        json_response_data = {'code': 1, 'msg': '拟合失败'}

    return HttpResponse(json.dumps(json_response_data))


def show_curve_result(request):
    return render_to_response('curve_result.html')


def show_cv_result(request):
    return render_to_response('cv_result.html')

def compute_cv(request):
    pass


def compute_error(request):
    pass


def save(request):
    pass


