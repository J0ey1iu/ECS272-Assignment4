from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
from sklearn import linear_model
import os
from Assignment4 import settings

# Create your views here.
def __test__(request):
    df = pd.read_csv(os.path.join(settings.BASE_DIR, 'student-mat.csv'))
    print(df.columns)

    reg = linear_model.LinearRegression()
    reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
    print(reg.coef_)

    return render(request, 'testpage.html') 