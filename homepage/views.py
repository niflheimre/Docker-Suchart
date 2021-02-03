from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import case
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
        template = loader.get_template('homepage/twitter_search.html')
        context = {
            'keyword': data['keyword'],
        }
        return HttpResponse(template.render(context, request))