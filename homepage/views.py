from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import case,Tweet
from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
import snscrape.modules.twitter as sntwitter
import copy
import pandas as pd
from .MLmaterial.MLmodel import Predict
import torch

# Create your views here.

def index(request):
    count = 0
    print(request.GET)
    if request.method == 'GET':
        return render(request, 'homepage/index.html')
    if request.method == 'POST':
        return render(request, 'homepage/index.html')

def raiseCase(request):

    if request.method == 'GET':
        return render(request, 'homepage/raiseCase.html')
    
    if request.method == 'POST':
        data = request.POST
        
        date = data['trans_date']

        if data['trans_date'] == '':
            date = None

        case.objects.create(
            bank_name = data['b_name'] if 'b_name' in data else None,
            bank_num = data['b_acc'] if 'b_acc' in data else None,
            details = data['detail'] if 'detail' in data else None,
            goods = data['goods'],
            nat_id = data['nat_id'] if 'nat_id' in data else None,
            name = data['name'],
            price = data['price'],
            province = data['province'] if 'province' in data else None,
            trans_date = date,
            website=data['website'] if 'website' in data else None
        )
        return render(request, 'homepage/case_added.html')

def modelSite(request):

    if request.method == 'GET':
        return render(request, 'homepage/predict.html')

# api/query?type=<str>&content=<str>
def caseExist(request):

    if request.method == 'GET':
        
        typ = request.GET.get('type')
        content = request.GET.get('content')
        
        obj = None

        if(typ == 'name'):
            obj = case.objects.filter(status='1').filter(name__contains=str(content)).values()
        if(typ == 'bank_num'):
            obj = case.objects.filter(status='1').filter(bank_num=content).values()
        if(typ == 'nat_id'):
            obj = case.objects.filter(status='1').filter(nat_id=content).values()
        
        if (len(obj) != 0):
            a = obj.order_by('-report_date')[0]
            return JsonResponse({"value": True,"count":len(obj),"last": a['report_date'].strftime("%B %d, %Y")}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"value": False}, status=status.HTTP_200_OK)
    
    return Response({"Error": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)

# api/model?text=<str>
def MLmodel(request):
    
    ###### rmem used prox 1.1 GB can't deploy on heroku :( ######

    if request.method == 'GET':
        print('request received.')

        postxt = request.GET.get('text')

        res = Predict(postxt,26)

        return JsonResponse({"result": str(res)}, status=status.HTTP_200_OK)
    
    ##############################################################
        
    return JsonResponse({"Error": "Forbidden Request"}, status=status.HTTP_403_FORBIDDEN)


def twitterSearch(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            # html = '<html><body></br></br></br><h1>This page is under maintenance.</h1><h4 id="countdown">Closing in 5 second."</h4></body><script>var seconds = 5;function countdown() {seconds = seconds - 1;if (seconds < 0) {window.close();} else {document.getElementById("countdown").innerHTML = "Closing in "+ seconds.toString() +" second.";window.setTimeout("countdown()", 1000);} } countdown();</script></html>'
            # return HttpResponse(html)
            
            return render(request, 'homepage/twitter_search.html')    # snscrape not working on AWS server :(
        else:
            return redirect('index')

    if request.method == 'POST' and request.user.is_authenticated:

        data = request.POST
        resultlist = {"result" : []}
        model = {
                "user":"",
                "text":"",
                "index":""
            }
        template = loader.get_template('homepage/twitter_search.html')

        if 'searchBtn' in data :
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(data['keyword'] + '(from:' + data['username'] + ')' +'since:2015-12-17').get_items()) :
                if i > int(data['maxtweets']) :
                    break

                jstweet = copy.deepcopy(model)
                jstweet['index'] = i
                jstweet['user'] = tweet.username
                jstweet['text'] = tweet.content
                resultlist['result'].append(jstweet)

        elif 'saveBtn' in data :
            saved_df = pd.DataFrame(columns=['user_name','text'])
            coluser = data.getlist('coluser')
            coltext = data.getlist('coltext')

            for index in range(len(data.getlist('coluser'))) :
                jstweet = copy.deepcopy(model)
                jstweet['index'] = index
                jstweet['user'] = coluser[index]
                jstweet['text'] = coltext[index]
                resultlist['result'].append(jstweet)

                if  'colindex' in data :
                    if str(index) in data.getlist('colindex'):
                        Tweet.objects.create(
                        user=coluser[index],
                        post=coltext[index]
                        )

                        # saved_df = saved_df.append({'user_name': coluser[index], 'text': coltext[index]},ignore_index=True)
            print(saved_df)
            
        elif 'saveAll' in data :
            saved_df = pd.DataFrame(columns=['user_name','text'])
            coluser = data.getlist('coluser')
            coltext = data.getlist('coltext')

            for index in range(len(data.getlist('coluser'))) :
                jstweet = copy.deepcopy(model)
                jstweet['index'] = index
                jstweet['user'] = coluser[index]
                jstweet['text'] = coltext[index]
                resultlist['result'].append(jstweet)

                Tweet.objects.create(
                    user=coluser[index],
                    post=coltext[index]
                    )
                # saved_df = saved_df.append({'user_name': coluser[index], 'text': coltext[index]},ignore_index=True)
            print(saved_df)
        return HttpResponse(template.render(resultlist, request))
