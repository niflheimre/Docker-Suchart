from ..models import case
from ..MLmaterial.MLmodel import Predict
from .tweetscrape import TweetIdScraper
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from threading import Thread
import time

class predictThread(Thread):

        def __init__(self, post):
            self.sText = 'time out'
            self.sPost = post
            self.super = super(predictThread, self).__init__(daemon=True)

        def run(self):
            print('predictThread start!')
            self.sText = Predict(self.sPost,26)
            print('predictThread finish!')
            return

class checkFunc():
    def check(reqjson, sessionID,host):
        resjson = {}
        resjson['fulfillmentMessages'] = [{'text': {'text': ["สามารถตรวจสอบได้จาก การกรอกแบบฟอร์ม ข้อมูลส่วนตัวผู้ขาย ข้อความจากโพสต์ผู้ขาย"]}},
        {'text': {'text': ["สามารถตรวจสอบได้จาก"]},'platform': "FACEBOOK"},
        {'text': {'text': ["การกรอกแบบฟอร์ม"]},'platform': "FACEBOOK"},
        {'text': {'text': ["ข้อมูลส่วนตัวผู้ขาย"]},'platform': "FACEBOOK"},
        {
            'quickReplies': {
            'title': "ข้อความจากโพสต์ผู้ขาย",
            'quickReplies': [
                "กรอกฟอร์ม","ข้อมูลส่วนตัวผู้ขาย","ข้อความโพส"
            ]
            },
            'platform': "FACEBOOK"
        }]
        resjson['outputContexts'] = [{
            "name": sessionID + '/contexts/check',
            "lifespanCount": 2,
            "parameters": reqjson.get('queryResult').get('parameters')
        }]
        
        return resjson

    def check_choice(reqjson, sessionID,host):
        resjson = {}
        print(host)
        if reqjson.get('queryResult').get('parameters').get('use_form'):
            resjson['fulfillmentMessages'] = [{'text': {'text': ["https://"+host+"/#search"]}},
            {
                'card': {
                    'title': "แบบฟอร์มตรวจสอบร้านค้าออนไลน์",
                    'imageUri': "https://"+host,
                    'buttons': [
                        {
                        "text": "ไปที่แบบฟอร์ม",
                        "postback": "https://"+host+"/#search"
                        }
                    ]
                },
                'platform': "FACEBOOK"
            }]
            resjson['fulfillmentText'] = "https://"+host+"/#search"
            resjson['outputContexts'] = [{
                "name": sessionID + '/contexts/check',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            }]

        elif reqjson.get('queryResult').get('parameters').get('use_post'):
            resjson['fulfillmentMessages'] = [{'text': {'text': ["ระบุข้อความโพสต์ขายของมาได้เลย"]}}]
            resjson['fulfillmentText'] = "ระบุข้อความโพสต์ขายของมาได้เลย"
            resjson['outputContexts'] = [{
                "name": sessionID + '/contexts/check_post',
                "lifespanCount": 1,
                "parameters": reqjson.get('queryResult').get('parameters')
            },{
                "name": sessionID + '/contexts/check',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            }]

        elif reqjson.get('queryResult').get('parameters').get('use_inform'):
            resjson['fulfillmentMessages'] = [{'text': {'text': ["ต้องการค้นหาจากข้อมูลอะไรครับ"]}},
                {'text': {'text': ["ต้องการค้นหาจากข้อมูลอะไรครับ"]},'platform': "FACEBOOK"},
                {
                    'quickReplies': {
                    'title': "ผมสามารถตรวจสอบได้จาก ชื่อ ,เลขประจำตัวประชาชน และ เลขบัญชีธนาคาร",
                    'quickReplies': [
                        "ชื่อ","เลขประจำตัวประชาชน","เลขบัญชีธนาคาร"
                    ]
                    },
                    'platform': "FACEBOOK"
                }]
            resjson['fulfillmentText'] = "ต้องการค้นหาจากข้อมูลอะไรครับ"
            resjson['outputContexts'] = [{
                "name": sessionID + '/contexts/check_inform',
                "lifespanCount": 2,
                "parameters": reqjson.get('queryResult').get('parameters')
            },{
                "name": sessionID + '/contexts/check',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            }]

        return resjson

    def check_post(reqjson, sessionID,host):
        resjson = {}
        post = str(reqjson.get('queryResult').get('parameters').get('post'))
        text = "time out"
        resjson['fulfillmentMessages'] = []
        
        validate = URLValidator()
        try:
            validate(post)
            urlsplit = post.replace('?', '/').split('/')
            try:
                tweetid = (urlsplit[urlsplit.index('status')+1] if urlsplit[urlsplit.index('status')+1].strip('0123456789') == '' else '')
                soup = TweetIdScraper(tweetID=tweetid).get_item()
            except:
                soup = None
            try:
                post = str(soup.find("meta", {"property": "og:description"})["content"])[1:-1]
                resjson['fulfillmentMessages'] = [{'text': {'text': [post]}}]
                
            except:
                text = 'invalid tweet url'
            p = predictThread(post)
            p.start()
            time.sleep(3)
            text = p.sText
        except ValidationError as e:
            p = predictThread(post)
            p.start()
            time.sleep(3)
            text = p.sText
        resjson['fulfillmentText'] = text
        resjson['fulfillmentMessages'].append({'text': {'text': [text]}})

        return resjson

    def check_inform(reqjson, sessionID,host):
        resjson = {}
        if reqjson.get('queryResult').get('parameters').get('use_name'):
            resjson['fulfillmentMessages'] = [{'text': {'text': ["บอกชื่อของคนขายมาได้เลย"]}}]
            resjson['fulfillmentText'] = "บอกชื่อของคนขายมาได้เลย"
            resjson['outputContexts'] = [{
                "name": sessionID + '/contexts/check_inform_name',
                "lifespanCount": 1,
                "parameters": reqjson.get('queryResult').get('parameters')
            },{
                "name": sessionID + '/contexts/check_inform',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            }]

        elif reqjson.get('queryResult').get('parameters').get('use_id'):
            resjson['fulfillmentMessages'] = [{'text': {'text': ["ขอทราบเลขประจำตัวประชาชนของคนขายด้วยครับ"]}}]
            resjson['fulfillmentText'] = "ขอทราบเลขประจำตัวประชาชนของคนขายด้วยครับ"
            resjson['outputContexts'] = [{
                "name": sessionID + '/contexts/check_inform_phone',
                "lifespanCount": 2,
                "parameters": reqjson.get('queryResult').get('parameters')
            },{
                "name": sessionID + '/contexts/check_inform',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            }]

        elif reqjson.get('queryResult').get('parameters').get('use_banknum'):
            resjson['fulfillmentMessages'] = [{'text': {'text': ["ขอทราบเลขที่บัญชีผู้ขายครับ"]}}]
            resjson['fulfillmentText'] = "ขอทราบเลขที่บัญชีผู้ขายครับ"
            resjson['outputContexts'] = [{
                "name": sessionID + '/contexts/check_inform_banknum',
                "lifespanCount": 2,
                "parameters": reqjson.get('queryResult').get('parameters')
            },{
                "name": sessionID + '/contexts/check_inform',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            }]

        else:
            name = str(reqjson.get('queryResult').get('parameters').get('seller_name'))
            id = str(reqjson.get('queryResult').get('parameters').get('seller_id'))
            banknum = str(reqjson.get('queryResult').get('parameters').get('seller_banknum'))
            
            obj = None

            text = ''
            resultlist = []
            resulttext = ''
            if name:
                text = 'ชื่อ: ' + name + '\n'
                obj = case.objects.filter(name__contains=str(name))
                if (len(obj)!=0):
                    if (len(obj)<2):
                        resultlist.append('ชื่อ: ' + str(obj[0])[2:] + '\nและ')
                    else :
                        resultlist.append('ชื่อ: ' + str(obj[0])[2:] + ' ,\n'
                        + str(obj[1])[2:] + '\n...\n')
                obj = None
            if id:
                text = text + 'เลขประจำตัวประชาชน: ' + id + '\n'
                obj = case.objects.filter(nat_id=str(id))
                if (len(obj)!=0):
                    resultlist.append('เลขประจำตัวประชาชน\n')
                obj = None
            if banknum:
                text = text + 'เลขบัญชี: ' + banknum + '\n'
                obj = case.objects.filter(bank_num=str(banknum))
                if (len(obj)!=0):
                    resultlist.append('เลขบัญชี\n')
                obj = None
            if resultlist:
                resulttext = 'พบข้อมูล\n' + "".join(resultlist) +'ของผู้มีประวัติโกงที่ตรงกัน'
            else :
                resulttext = 'ไม่พบข้อมูลของผู้มีประวัติโกงที่ตรงกัน'

            resjson['fulfillmentMessages'] = [{'text': {'text': [resulttext]}},
            {'text': {'text': [text]},'platform': "FACEBOOK"},
            {'text': {'text': [resulttext]},'platform': "FACEBOOK"},]
            resjson['outputContexts'] = [{
                "name": sessionID + '/contexts/check_inform',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            }]
        
        return resjson

    def check_inform_more(reqjson, sessionID,host):
        resjson = {}
        resjson['fulfillmentMessages'] = [{'text': {'text': ["ต้องการแก้ไขหรือเพิ่มข้อมูลอะไรอีกไหม"]}},
            {
                'quickReplies': {
                'title': "ต้องการแก้ไขหรือเพิ่มข้อมูลอะไรอีกไหม",
                'quickReplies': [
                    "ชื่อ","เลขประจำตัวประชาชน","เลขบัญชีธนาคาร","ไม่ต้องการ"
                ]
                },
                'platform': "FACEBOOK"
            }]
        resjson['fulfillmentText'] = "ต้องการแก้ไขหรือเพิ่มข้อมูลอะไรอีกไหม"
        resjson['outputContexts'] = [{
                "name": sessionID + '/contexts/check_inform',
                "lifespanCount": 2,
                "parameters": reqjson.get('queryResult').get('parameters')
            },{
                "name": sessionID + '/contexts/check_inform_banknum',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            },{
                "name": sessionID + '/contexts/check_inform_phone',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            }]
        return resjson