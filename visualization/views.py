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

# def index(request):
#     df = pd.read_csv(os.path.join(settings.BASE_DIR, 'pokemon_alopez247.csv'))
#     cluster_filtered = df.loc[:, ['Attack', 'Defense']]
#     data = []
#     for i in range(len(cluster_filtered)):
#         data.append([cluster_filtered['Attack'][i], cluster_filtered['Defense'][i]])
#     kmeans = KMeans(n_clusters=4).fit(data)
#     cluster_filtered['Cluster'] = kmeans.labels_
#     cluster_ret = {}
#     cluster_ret['Attack'] = list(cluster_filtered['Attack'])
#     cluster_ret['Defense'] = list(cluster_filtered['Defense'])
#     cluster_ret['Cluster'] = list(cluster_filtered['Cluster'])
        
#     columns = ['Type_1', 'Generation', 'Color', 'Body_Style']
#     sandkey_filtered = df.loc[:, columns]
#     sandkey_filtered = sandkey_filtered.fillna('None')
#     nodes = []
#     nodes_ = []
#     for i in range(len(columns)):
#         if columns[i] == 'Generation':
#             uni = [int(v) for v in list(sandkey_filtered[columns[i]].unique())]
#             nodes.append(uni)
#             for key in uni:
#                 nodes_.append({
#                     'id': key
#                 })
#             continue
#         uni = list(sandkey_filtered[columns[i]].unique())
#         nodes.append(uni)
#         for key in uni:
#             nodes_.append({
#                 'id': key
#             })
        
#     links = []
#     for i in range(len(columns)-1):
#         sources = nodes[i]
#         targets = nodes[i+1]
#         for j in range(len(nodes[i])):
#             for k in range(len(nodes[i+1])):
#                 links.append({
#                     'source': nodes[i][j],
#                     'target': nodes[i+1][k],
#                     'value': len(sandkey_filtered.loc[(sandkey_filtered[columns[i]] == nodes[i][j]) & (sandkey_filtered[columns[i+1]] == nodes[i+1][k])])
#                 })
    
#     sandkey_ret = {'nodes': nodes_, 'links': links}

#     x = [int(v) for v in df['Speed']]
#     hist_ret = {'x': x}

#     data = {'cluster': cluster_ret, 'sandkey': sandkey_ret, 'histogram': hist_ret}

#     return render(request, 'visualization.html', data)


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

def getk(request):
    k = request.GET.get('k', None)
    data = {
        'success': 0
    }
    return JsonResponse(data)

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