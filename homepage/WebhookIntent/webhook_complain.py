

class complainFunc():
    def complain(reqjson, sessionID):
        resjson = {}
        resjson['fulfillmentMessages'] = [{'text': {'text': ["https://web.suchart.info/new_case/"]}},
        {
            'card': {
                'title': "แบบฟอร์มร้องเรียนร้านค้าออนไลน์",
                'imageUri': "https://suchart-webhook.herokuapp.com/img/Newcasepage.jpg",
                'buttons': [
                    {
                        "text": "ไปที่แบบฟอร์ม",
                        "postback": "https://web.suchart.info/new_case/"
                    }
                    ]
            },
            'platform': "FACEBOOK"
        }]
        resjson['fulfillmentText'] = "https://web.suchart.info/new_case/"
            
        return resjson
