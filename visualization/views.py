from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
import json
import pandas as pd
from sklearn import linear_model
import os
from Assignment4 import settings

# Create your views here.
def __test__(request):
    df = pd.read_csv(os.path.join(settings.BASE_DIR, 'student-mat.csv'))

    reg = linear_model.LinearRegression()
    reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
    print(reg.coef_)

    return render(request, 'testpage.html', 
        {'coef': reg.coef_})

def getGenderRatio(request):
    df = pd.read_csv(os.path.join(settings.BASE_DIR, 'student-mat.csv'))
    numbers = [len(df[df.sex == 'F']), len(df[df.sex == 'M'])]
    labels = ['female', 'male']
    res = {'numbers': numbers, 'labels': labels}
    return JsonResponse(res)

def ajaxTest(request):
    if request.is_ajax():
        print('Got the request!')
        res = ['aaa', 'bbb']
        data = json.dumps(res)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404