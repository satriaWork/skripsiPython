# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 20:39:24 2019

@author: MUHAMAD SATRIA ADHI
"""

#program untuk menguji akurasi dataset 

import pandas as pd

data = pd.read_csv('./data_set/1tweetTest.csv')



import pandas as pd

raw_data2 = pd.DataFrame()
tmp=pd.read_csv('./data_set/1tweetTrainLabel.csv')
raw_data2 = raw_data2.append(tmp,ignore_index=True)



#raw_data to list
Dataset = raw_data2[['text','kelas']].values.tolist()

#pisahkan text dan labelnya
Texts = [col[0] for col in Dataset]
Labels = [col[1] for col in Dataset]



for i in data['text']:
    Texts.append(i)



from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)
tfidf = tfidf_vectorizer.fit_transform(Texts)

matrix_tfidf = tfidf.toarray()



total_data_training = len(Dataset)

x_train = matrix_tfidf[0:total_data_training,]
x_test = matrix_tfidf[total_data_training:len(Texts),]



from sklearn.naive_bayes import MultinomialNB
mnb = MultinomialNB()
model = mnb.fit(x_train, Labels)



predict = model.predict(x_test)

import pandas as pd
raw_data = pd.DataFrame()
tmp = pd.read_csv('./data_set/1tweetTestLabel.csv')
raw_data = raw_data.append(tmp,ignore_index=True)

Dataset = raw_data[['text','kelas']].values.tolist()

kelas = [col[1] for col in Dataset]


from sklearn.metrics import accuracy_score
print(accuracy_score(kelas,predict))