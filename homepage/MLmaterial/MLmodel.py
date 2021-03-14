from pythainlp.tokenize import word_tokenize
from pythainlp.util import rank,dict_trie
from pythainlp.corpus.common import thai_words
from simpletransformers.classification import ClassificationModel
from transformers import BertForSequenceClassification
import torch
import numpy as np
import gc
from django.conf import settings 

def LoadModel():

    gc.collect()

    model_args = {
        'no_cache': True,
        'no_save':True
    }

    try:

        settings.my_ml_model_variable = ClassificationModel(
            "bert", './homepage/MLmaterial/weightedModel', use_cuda=False,args=model_args
        )
        # model = BertForSequenceClassification.from_pretrained('./homepage/MLmaterial/weightedModel')

        print('model created.')

    except:
        return "Error loading model"

    cusset = set(thai_words())

    with open('./homepage/MLmaterial/testread.txt', 'r', encoding='utf8') as f:
        for a in f.read().splitlines():
            cusset.add(a)
    settings.cusset = cusset
    del cusset


def Predict(text,treshold):
    userinput = []
    
    input = ' '.join(word_tokenize(text, engine='newmm', custom_dict=dict_trie(dict_source=settings.cusset)))
    
    userinput.append(input)

    output = settings.my_ml_model_variable.predict((userinput))

    pred = "มีโอกาสโดนหลอกมากนะ" if np.any(output[1] >= treshold) else "มีโอกาสโดนหลอกน้อยนะ"

    gc.collect()
    
    del output
    del input
    del userinput

    return pred
