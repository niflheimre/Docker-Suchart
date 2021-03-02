

class complainFunc():
    def complain(reqjson, sessionID):
        resjson = {}
        resjson['fulfillmentMessages'] = [{'text': {'text': ["https://suchart-docker.herokuapp.com/new_case/?fbclid=IwAR2LV7kgh89ku55vFjhUd6P2_yqmqwB78XpXQ_p26hXon4AWECc_Erge16w"]}},
        {
            'card': {
                'title': "แบบฟอร์มร้องเรียนร้านค้าออนไลน์",
                'imageUri': "https://suchart-webhook.herokuapp.com/img/Newcasepage.jpg",
                'buttons': [
                    {
                        "text": "ไปที่แบบฟอร์ม",
                        "postback": "https://suchart-docker.herokuapp.com/new_case/?fbclid=IwAR2LV7kgh89ku55vFjhUd6P2_yqmqwB78XpXQ_p26hXon4AWECc_Erge16w"
                    }
                    ]
            },
            'platform': "FACEBOOK"
        }]
        resjson['fulfillmentText'] = "https://suchart-docker.herokuapp.com/new_case/?fbclid=IwAR2LV7kgh89ku55vFjhUd6P2_yqmqwB78XpXQ_p26hXon4AWECc_Erge16w"
            
        return resjson
