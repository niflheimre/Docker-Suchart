from ..MLmaterial.MLmodel import Predict

class checkFunc():
    def check(reqjson, sessionID):
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

    def check_choice(reqjson, sessionID):
        resjson = {}
        if reqjson.get('queryResult').get('parameters').get('use_form'):
            resjson['fulfillmentMessages'] = [{'text': {'text': ["http://suchart-docker.herokuapp.com/#search"]}},
            {
                'card': {
                    'title': "แบบฟอร์มตรวจสอบร้านค้าออนไลน์",
                    'imageUri': "https://suchart-webhook.herokuapp.com/img/Checkpage.jpg",
                    'buttons': [
                        {
                        "text": "ไปที่แบบฟอร์ม",
                        "postback": "http://suchart-docker.herokuapp.com/#search"
                        }
                    ]
                },
                'platform': "FACEBOOK"
            }]
            resjson['fulfillmentText'] = "http://suchart-docker.herokuapp.com/#search"
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
                    'title': "ผมสามารถตรวจสอบได้จาก ชื่อ ,เบอร์โทรศัพท์ และ เลขบัญชีธนาคาร",
                    'quickReplies': [
                        "ชื่อ","เบอร์โทรศัพท์","เลขบัญชีธนาคาร"
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

    def check_post(reqjson, sessionID):
        ########################################### !!! mock up !!!
        resjson = {}
        post = reqjson.get('queryResult').get('parameters').get('post')
        text = "time out"
        text = Predict(post,26)
        resjson['fulfillmentText'] = text
        resjson['fulfillmentMessages'] = [{'text': {'text': [text]}}]
        return resjson

    def check_inform(reqjson, sessionID):
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

        elif reqjson.get('queryResult').get('parameters').get('use_phonenum'):
            resjson['fulfillmentMessages'] = [{'text': {'text': ["ขอทราบเบอร์โทรศัพท์ของคนขายด้วยครับ"]}}]
            resjson['fulfillmentText'] = "ขอทราบเบอร์โทรศัพท์ของคนขายด้วยครับ"
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
            ########################################### !!! mock up !!!
            name = str(reqjson.get('queryResult').get('parameters').get('seller_name'))
            phone = str(reqjson.get('queryResult').get('parameters').get('seller_phone'))
            banknum = str(reqjson.get('queryResult').get('parameters').get('seller_banknum'))
            text = ''
            if name:
                text = 'ชื่อ: ' + name + '\n'
            if phone:
                text = text + 'เบอร์โทร: ' + phone + '\n'
            if banknum:
                text = text + 'เลขบัญชี: ' + banknum + '\n'
            resjson['fulfillmentMessages'] = [{'text': {'text': [text]}},
            {'text': {'text': [text]},'platform': "FACEBOOK"},
            {
            'text': {
                'text': ['ไม่โกง']
            },'platform': "FACEBOOK"
            }]
            resjson['outputContexts'] = [{
                "name": sessionID + '/contexts/check_inform',
                "lifespanCount": 0,
                "parameters": reqjson.get('queryResult').get('parameters')
            }]
        
        return resjson

    def check_inform_more(reqjson, sessionID):
        resjson = {}
        resjson['fulfillmentMessages'] = [{'text': {'text': ["ต้องการแก้ไขหรือเพิ่มข้อมูลอะไรอีกไหม"]}},
            {
                'quickReplies': {
                'title': "ต้องการแก้ไขหรือเพิ่มข้อมูลอะไรอีกไหม",
                'quickReplies': [
                    "ชื่อ","เบอร์โทรศัพท์","เลขบัญชีธนาคาร","ไม่ต้องการ"
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