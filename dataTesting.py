# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 19:48:54 2019

@author: MUHAMAD SATRIA ADHI
"""
#program untuk Preprocessing data testing

import codecs, json
with codecs.open('./data_set/tweetsFix.json','r','utf-8') as f:
    tweets=json.load(f, encoding='utf-8')




import re
kumpText=[]
def preprocessing(text="",
                  casefolding=True,
                  removeusername=True,
                  removenonalphabet=True,
                  removestopword=True,
                  stemming=True,
                  removehashtag=True,
                  removeemail=True,
                  removeAdr=True):
    
    if(text!=""):
        import re
       
        if(casefolding):
            text = text.lower()
            
        if(removeusername):
            nama = re.compile("(?:^|\s)[＠ @]{1}([^\s#<>[\]|{}]+)", re.UNICODE)
            text = re.sub(nama, ' ', text)

        
        if(removeAdr):
            com= re.compile(r' \w+\.\w+\.*\w*\D\w*')
            text = re.sub(com, ' ', text)
            
        if(removehashtag):
            hashtag = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)
            text = re.sub(hashtag, ' ', text)
 
        if(removeemail):
            email = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
            text = re.sub(email, ' ', text) 
            
        if(removenonalphabet):
            import re
            text = ' '.join(re.findall(r'\b[a-z]+?[a-z]+\b',text))
    
        if(removestopword):
            from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
            factory = StopWordRemoverFactory()
            Sastrawi_StopWords_id = factory.get_stop_words()
            temp = [t for t in re.findall(r'\b[a-z]+-?[a-z]+\b',text) if t not in Sastrawi_StopWords_id]
            text = ' '.join(temp)
            
        if(stemming):
            from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
            stemmer = StemmerFactory().create_stemmer()
            text   = stemmer.stem(text)
            
    return(text)



import json

filejson=open("./data_set/tweetsFix.json")
data=json.loads(filejson.read())
komentar = []
kata=[]
for item in data[420:700]:
    r={}
    r['text'] = preprocessing(item['text'])
    komentar.append(r)
    tweet=r['text'] if 'text' in item else item
    
    
    file = open("kamus.txt", encoding="utf-8", errors='replace')
    Teks = file.readlines()
    Teks_string=' '.join(Teks)
    fix=eval(Teks_string)
    
    t=" ",tweet," "
    t_string=' '.join(t)
    t_jadi=t_string 
    
    for slang, formal in fix.items():
        t_jadi = t_jadi.replace(slang,formal)
    kata.append(t_jadi)

import requests
import nlp_if_lib as nlp
import urllib, json
import re
from spacy.lang.id import Indonesian

nlp_id_spacy = Indonesian() 


kataJadi=[] 
lenKata=len(kata)
for t in range(0,lenKata):
    teksAnt=[]
    kataStrip=kata[t].strip()
    kataToken = nlp_id_spacy(kataStrip)  
    token_pos = nlp.getPOSTag()
    
    for x in kataToken:
        teksAnt.append(x.text)
    
    lenTeksAnt=len(teksAnt)   
    for y in range(0,lenTeksAnt):
        antonim=[]
        if(teksAnt[y]=="tidak" or teksAnt[y]=="kurang" or teksAnt[y]=="belum"):
            for token in kataToken:
                t=token.lemma_
                try: 
                    pos=token_pos[token.lemma_]
                    if(token_pos[teksAnt[y+1]]=="adj"):
                        url = "http://kateglo.com/api.php?format=json&phrase="+teksAnt[y+1]
                        response = requests.get(url)
                        data=response.text
                        parsed=json.loads(data)

                        post = parsed["kateglo"]["relation"]["a"]
                        lenPost=len(post)
                        for x in range(0,lenPost):
                            st=str(x)
                            value=post[st]
                            if(value['rel_type']=='a'):
                                if(value['lex_class']=='adj'):
                                    ant=value['related_phrase']
                                    antonim.append(ant)
                                    teksAnt[y+1]=""
                                    teksAnt[y]=""

                except:
                    pos='n'

                
        print(antonim)    
        listAnt=len(antonim)
        for i in range(0,listAnt):
            teksAnt.append(antonim[i])
        
    ubahAnt=' '.join(teksAnt)
    kataJadi.append(ubahAnt)


lenKata=len(kataJadi)
kataS=[]
for s in range(0,lenKata):
    st=kataJadi[s].strip()
    kataS.append(st)
    
lenKataS=len(kataS)    
for i in range(0,lenKataS):
    for j in range(i+1,lenKataS):
        if(kataS[i]==kataS[j]):
            kataS[j]=""

for h in kataS:
    if(h==""):
        kataS.remove(h)


import pandas as pd

dt = pd.DataFrame(kataS, columns=['text'])

dt.to_csv("./data_set/1tweetTest.csv",  encoding='utf-8', index=False) 