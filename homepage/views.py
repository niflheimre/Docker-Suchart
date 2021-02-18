from django.shortcuts import render
from .models import case
from rest_framework import status
from django.http.response import JsonResponse

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

# api/query?type=<str>&content=<str>
def caseExist(request):

    if request.method == 'GET':
        
        typ = request.GET.get('type')
        content = request.GET.get('content')
        
        obj = None

        if(typ == 'name'):
            obj = case.objects.filter(name__contains=str(content))
        if(typ == 'bank_num'):
            obj = case.objects.filter(bank_num=content)
        if(typ == 'nat_id'):
            obj = case.objects.filter(nat_id=content)
        
        if (len(obj)!=0):
            return JsonResponse({"value": True,"count":len(obj)}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"value": False},status=status.HTTP_200_OK)
            

