

class complainFunc():
    def complain(reqjson, sessionID,host):
        resjson = {}
        resjson['fulfillmentMessages'] = [{'text': {'text': ["https://"+host+"/new_case"]}},
        {
            'card': {
                'title': "แบบฟอร์มร้องเรียนร้านค้าออนไลน์",
                'imageUri': "https://"+host,
                'buttons': [
                    {
                        "text": "ไปที่แบบฟอร์ม",
                        "postback": "https://"+host+"/new_case"
                    }
                    ]
            },
            'platform': "FACEBOOK"
        }]
        resjson['fulfillmentText'] = "https://"+host+"/new_case/"
            
        return resjson
