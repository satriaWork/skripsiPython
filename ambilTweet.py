# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:56:15 2019

@author: MUHAMAD SATRIA ADHI
"""

import codecs, json
with codecs.open('./data_set/tweetsFix.json','r','utf-8') as f:
    text=json.load(f, encoding='utf-8')

import json
filejson=open("./data_set/tweetsFix.json")
data=json.loads(filejson.read())
komentar = []
for item in data[0:419]:
    komentar.append(item['text'])
    
lenKata=len(komentar)
for i in range(0,lenKata):
    for j in range(i+1,lenKata):
        if(komentar[i]==komentar[j]):
            komentar[j]=""

for h in komentar:
    if(h==""):
        komentar.remove(h)

    
import pandas as pd
dt = pd.DataFrame(komentar, columns=['text'])
dt.to_csv("./data_set/1Tweets.csv",  encoding='utf-8', index=False)