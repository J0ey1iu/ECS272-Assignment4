from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def __test__(request):
    return render(request, 'testpage.html')