# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 05:24:48 2019

@author: MUHAMAD SATRIA ADHI
"""

#program untuk preprocessing data testing dengan Query Expansion

from urllib.request import urlopen
from bs4 import BeautifulSoup
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


#ANTONIM
import nlp_if_lib as nlp
import json
from spacy.lang.id import Indonesian
import requests
nlp_id_spacy = Indonesian() 

nonEx=[]
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
        if(teksAnt[y]=="tidak" or teksAnt[y]=="belum" or teksAnt[y]=="kurang"):
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
                                
                    nonEx.append(teksAnt[y+1])#contoh kata "Tanggap"
                        
                except:
                    pos='n'
            
        
            
        listAnt=len(antonim)
        for i in range(0,listAnt):
            teksAnt.append(antonim[i])
        
    ubahAnt=' '.join(teksAnt)
    kataJadi.append(ubahAnt)


lenKata=len(kataJadi) 
kataS=[]
for s in range(0,lenKata):
    st=kataJadi[s].strip()
    subs=re.sub(' +', ' ',st)
    kataS.append(subs)
    
    
lenKataS=len(kataS)
for i in range(0,lenKata):
    for j in range(i+1,lenKata):
        if(kataS[i]==kataS[j]):
            kataS[j]=""

for h in kataS:
    if(h==""):
        kataS.remove(h)
        
        
        

import json
import nlp_if_lib as nlp
from spacy.lang.id import Indonesian

nlp_id_spacy = Indonesian() 
kataEx=[]
#Teks=kataToken,tweet=kataStrip

lenKataS=len(kataS)
for i in range(0,lenKataS):
    sinonim=[]
    teksA=[]
    kataStrip=kataS[i].strip()
    kataTokens = nlp_id_spacy(kataStrip)  
    token_pos = nlp.getPOSTag()
    
    for x in kataTokens:#tokenisasi tweet
        teksA.append(x.text)
    
    for tokens in kataTokens:
        try:
            pos=token_pos[tokens.lemma_]
            if(token_pos[tokens.lemma_]=="adj"):
                kataAdj=tokens.lemma_
                
                lenNon=len(nonEx)
                p=0
                for n in range(0,lenNon):
                    if(kataAdj==nonEx[n]):
                        p=p+1
                
                if(p==0):
                    url = "http://kateglo.com/api.php?format=json&phrase="+kataAdj  

                    respon = requests.get(url)
                    data=respon.text
                    dataSyn=json.loads(data)
                    

                    post = dataSyn["kateglo"]["all_relation"]
                    lenPost=len(post)
                    for x in range(0,lenPost):
                        value=post[x]
                        if(value['rel_type']=='s'):
                            if(value['lex_class']=='adj'):
                                syn=value['related_phrase']
                                sinonim.append(syn)

        except:
            pos='n'
             
        
    print(sinonim) 
    listSyn=len(sinonim)
    for z in range(0,listSyn):
        teksA.append(sinonim[z])
    
    queryEx=' '.join(teksA)
    kataEx.append(queryEx)

    
import pandas as pd

dt = pd.DataFrame(kataEx, columns=['text'])

dt.to_csv("./data_set/1tweetTestEx.csv",  encoding='utf-8', index=False)