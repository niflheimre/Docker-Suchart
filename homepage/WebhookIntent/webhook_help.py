
class helpFunc():
    def help(reqjson, sessionID):
        resjson = {}
        resjson['fulfillmentMessages'] = [{'text': {'text': ["ต้องการร้องเรียน หรือ ตรวจสอบ"]}},
        {
            'quickReplies': {
            'title': "ต้องการร้องเรียน หรือ ตรวจสอบ",
            'quickReplies': [
                "ร้องเรียน","ตรวจสอบ"
            ]
            },
            'platform': "FACEBOOK"
        }]
        resjson['fulfillmentText'] = "ต้องการร้องเรียน หรือ ตรวจสอบ"
        
        return resjson