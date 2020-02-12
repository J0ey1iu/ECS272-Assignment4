from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
import json
import pandas as pd
from sklearn.cluster import KMeans
import os
from Assignment4 import settings

# Create your views here.
def __test__(request):
    return render(request, 'visualization.html')

def getGenderRatio(request):
    if not request.is_ajax():
        raise Http404
    else:
        df = pd.read_csv(os.path.join(settings.BASE_DIR, 'pokemon_alopez247.csv'))
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

def cluster(request):
    if request.is_ajax():
        df = pd.read_csv(os.path.join(settings.BASE_DIR, 'pokemon_alopez247.csv'))
        filtered = df.loc[:, ['Attack', 'Defense']]
        data = []
        for i in range(len(filtered)):
            data.append([filtered['Attack'][i], filtered['Defense'][i]])
        kmeans = KMeans(n_clusters=4).fit(data)
        filtered['Cluster'] = kmeans.labels_
        ret = {}
        ret['Attack'] = list(filtered['Attack'])
        ret['Defense'] = list(filtered['Defense'])
        ret['Cluster'] = list(filtered['Cluster'])
        return JsonResponse(ret)
    else:
        raise Http404

def sandkey(request):
    if request.is_ajax():
        df = pd.read_csv(os.path.join(settings.BASE_DIR, 'pokemon_alopez247.csv'))
        columns = ['Type_1', 'Generation', 'Color', 'Body_Style']
        filtered = df.loc[:, columns]
        filtered = filtered.fillna('None')
        nodes = []
        nodes_ = []
        for i in range(len(columns)):
            if columns[i] == 'Generation':
                uni = [int(v) for v in list(filtered[columns[i]].unique())]
                nodes.append(uni)
                for key in uni:
                    nodes_.append({
                        'id': key
                    })
                continue
            uni = list(filtered[columns[i]].unique())
            nodes.append(uni)
            for key in uni:
                nodes_.append({
                    'id': key
                })
            
        links = []
        for i in range(len(columns)-1):
            sources = nodes[i]
            targets = nodes[i+1]
            for j in range(len(nodes[i])):
                for k in range(len(nodes[i+1])):
                    links.append({
                        'source': nodes[i][j],
                        'target': nodes[i+1][k],
                        'value': len(filtered.loc[(filtered[columns[i]] == nodes[i][j]) & (filtered[columns[i+1]] == nodes[i+1][k])])
                    })
        
        ret = {'nodes': nodes_, 'links': links}
        print(ret)
        return JsonResponse(ret)
    else:
        raise Http404

def histogram(request):
    if request.is_ajax():
        df = pd.read_csv(os.path.join(settings.BASE_DIR, 'pokemon_alopez247.csv'))
        x = [int(v) for v in df['Speed']]
        ret = {'x': x}
        return JsonResponse(ret)
    else:
        raise Http404