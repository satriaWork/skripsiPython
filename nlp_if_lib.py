# -*- coding: utf-8 -*-
"""
@author: Muhammad Zidny Naf'an
@email : zidny@ittelkom-pwt.ac.id
"""
import re
from collections import Counter
import PyPDF2
import docx2txt
from unidecode import unidecode
from wordcloud import WordCloud

#load txt file to string python
def loadTXT(path):
    #membaca file teks
    File = open(path, encoding="utf-8", errors='replace')
    Teks = File.readlines()
    File.close()
    del File
    return(' '.join(Teks))

#load pdf file to string python
def loadPDF(path):
    pdfFileObj = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    allText = ""
    for page_number in range(pdfReader.getNumPages()):
        page = pdfReader.getPage(page_number)
        page_content = page.extractText()
        allText += page_content
    return(''.join(allText))

#load docx file to string python
def loadDOCX(path):
    text = docx2txt.process(path)
    return(text)
        
def getPOSTag(path = 'data/kata_dasar.txt'):
    token_pos = {}
    df=open(path,"r",encoding="utf-8", errors='replace')
    lines=df.readlines();
    df.close()
    for line in lines:
        d = line.split()
        token = d[0].strip()
        pos = d[-1].strip().replace("(",'').replace(')','')
        token_pos[token] = pos
    return token_pos

#sumber: Sutanto, TSusanto_lib.py, Workshop Text Mining ITTC UAD 2018
#
def WordNetID(file1='data/wn-ind-def.tab', file2='data/wn-msa-all.tab'):
    definisi, wn_id = {}, {}
    df=open(file1,"r",encoding="utf-8", errors='replace')
    d1=df.readlines();df.close()
    df=open(file2,"r",encoding="utf-8", errors='replace')
    d2=df.readlines();df.close(); del df
    for line in d1:
        data = line.split('\t')
        definisi[data[0].strip()] = data[2].strip()
    for line in d2:
        data = line.split('\t')
        kata = data[3].strip()
        kode = data[0].strip()
        if data[1].strip()!="M" :
            if kode in definisi.keys():
                if kata in wn_id:
                    wn_id[kata]['def'].append(definisi[kode])
                    wn_id[kata]['pos'].append(kode[-1])
                else:
                    wn_id[kata] = {}
                    wn_id[kata]['def'] = [definisi[kode]]
                    wn_id[kata]['pos'] = [kode[-1]]
    return wn_id

#Norvig spell checker
#https://norvig.com/spell-correct.html
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('data/kata_dasar_non_pos.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
#end of norvig spell checker
    
#WordCloud
#source: https://github.com/amueller/word_cloud/blob/master/examples/simple.py
def wordCloud(text, file='wordcloud.png'):
    # Generate a word cloud image
    wordcloud = WordCloud(background_color="white").generate(text)
    
    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    #plt.imshow(wordcloud, interpolation='bilinear')
    #plt.axis("off")
    
    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    # The pil way (if you don't have matplotlib)
    image = wordcloud.to_image()
    image.show()