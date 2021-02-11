from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import case
import snscrape.modules.twitter as sntwitter
import copy
import pandas as pd
import json
# Create your views here.

def index(request):
    print(request.GET)
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
            bank_name = data['b_name'],
            bank_num = data['b_acc'],
            details = data['detail'],
            goods = data['goods'],
            nat_id = data['nat_id'],
            name = data['name'],
            price = data['price'],
            province = data['province'],
            trans_date = date,
            website=data['website']
        )
        return render(request, 'homepage/case_added.html')

def twitterSearch(request):

    if request.method == 'GET':
        return render(request, 'homepage/twitter_search.html')

    if request.method == 'POST':
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
                    if str(index) in data.getlist('colindex') :
                        saved_df = saved_df.append({'user_name': coluser[index], 'text': coltext[index]},ignore_index=True)
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
                saved_df = saved_df.append({'user_name': coluser[index], 'text': coltext[index]},ignore_index=True)
            print(saved_df)
        return HttpResponse(template.render(resultlist, request))
