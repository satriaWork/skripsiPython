# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 19:08:43 2019

@author: MUHAMAD SATRIA ADHI
"""
#Program untuk mengambil twit untuk data testing


import codecs, json
with codecs.open('./data_set/tweetsFix.json','r','utf-8') as f:
    text=json.load(f, encoding='utf-8')

import json
filejson=open("./data_set/tweetsFix.json")
data=json.loads(filejson.read())
komentar = []
for item in data[420:700]:
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
dt.to_csv("./data_set/Tweets2.csv",  encoding='utf-8', index=False)