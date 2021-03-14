from django.http.response import JsonResponse
import json
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from .WebhookIntent.webhook_help import helpFunc
from .WebhookIntent.webhook_complain import complainFunc
from .WebhookIntent.webhook_check import checkFunc

@csrf_exempt
def dialogflow(req):
    resjson = {}
    if req.method == 'POST':

        # Decode UTF-8 bytes to Unicode, and convert single quotes 
        # to double quotes to make it valid JSON
        reqjson = req.body.decode('utf8').replace("'", '"')

        # Load the JSON to a Python list & dump it back out as formatted JSON
        reqjson = json.loads(reqjson)
        '''
        if reqjson.get('originalDetectIntentRequest').get('payload').get('data') :
            senderID = reqjson.get('originalDetectIntentRequest').get('payload').get('data')\
                .get('sender').get('id')
            fbtoken = os.environ.get('FACEBOOK_PAGE_API_KEY')
            #docs https://developers.facebook.com/docs/messenger-platform/identity/user-profile
            url = "https://graph.facebook.com/v6.0/" + senderID + "?fields=first_name,last_name&access_token=" + fbtoken
            response = requests.get(url)
            #print(response.json())
        '''
        intentName = reqjson.get('queryResult').get('intent').get('displayName')
        if intentName == "help":
            resjson = helpFunc.help(reqjson, reqjson.get('session'))
        elif intentName == "complain":
            resjson = complainFunc.complain(reqjson, reqjson.get('session'))
        elif intentName == "check":
            resjson = checkFunc.check(reqjson, reqjson.get('session'))
        elif intentName == "check-choice":
            resjson = checkFunc.check_choice(reqjson, reqjson.get('session'))
        elif intentName == "check-post":
            resjson = checkFunc.check_post(reqjson, reqjson.get('session'))
        elif intentName == "check-inform":
            resjson = checkFunc.check_inform(reqjson, reqjson.get('session'))
        elif intentName == "check-inform-name":
            resjson = checkFunc.check_inform_more(reqjson, reqjson.get('session'))
        elif intentName == "check-inform-id":
            resjson = checkFunc.check_inform_more(reqjson, reqjson.get('session'))
        elif intentName == "check-inform-banknum":
            resjson = checkFunc.check_inform_more(reqjson, reqjson.get('session'))
            
        #resjson['fulfillmentMessages'] = [{'text': {'text': ["heloo"]}}]
        return JsonResponse(resjson, status=status.HTTP_200_OK)