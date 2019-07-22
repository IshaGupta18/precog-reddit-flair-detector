from __future__ import print_function
from flask import Flask, request, url_for
from flask_pymongo import PyMongo
import pymongo
import praw
import os
import re
import string
import nltk
import sys
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
reddit=praw.Reddit(client_id="GXSJ2q3iO6H1sw", client_secret="4HcvsdQ14CZMKRp1__ZkjkRnXGE",
                     password="ishagupta18", user_agent='testing praw',
                     username="isha_gupta18")
app = Flask(__name__)
app.config['MONGO_URI']="mongodb://gdgnd:gdgnd19@ds119755.mlab.com:19755/gdgndnodeangular"
mongo = PyMongo(app)
accuracy1=0
accuracy2=0
accuracy3=0
hash_labels={}
allLabels=[]
temparr=[]
m1=pickle.load(open("./titleModeldump.pkl", "rb"))
m2=pickle.load(open("./bodyModeldump.pkl", "rb"))
m3=pickle.load(open("./title_bodyModeldump.pkl", "rb"))
vectorizers=[m1[1],m2[1],m3[1]]
acc=[m1[2],m2[2],m3[2]]
reverse_hash_labels=m1[3]
def detectFlair(detectData):
    model1=m1[0]
    model2=m2[0]
    model3=m3[0]
    ans1 = model1.predict(detectData[0])
    ans2=model2.predict(detectData[1])
    ans3=model3.predict(detectData[2])
    d={}
    l=[ans1[0],ans2[0],ans3[0]]
    for i in range(len(l)):
        if l[i] not in d:
            d[l[i]]=[0,acc[i],l[i]]
        else:
            d[l[i]][0]+=1
    arr=[]
    for i in d:
        arr.append(d[i])
    arr.sort(key=lambda x: (-x[0],-x[1]))
    return reverse_hash_labels[arr[0][2]]
def createVector(data,vectorizer):
    stop_words=set(stopwords.words('english'))
    stemmer=PorterStemmer()
    lemmatizer=WordNetLemmatizer()
    for j in range(len(data)):
        temp=data[j].lower()
        temp=re.sub(r'\d+', '', temp)
        tempstr=""
        for char in temp:
            if char not in string.punctuation:
                tempstr+=char
        temp=tempstr
        temp=temp.strip()
        t=word_tokenize(temp)
        temp=[k for k in t if not k in stop_words]
        temp2=[stemmer.stem(word=word) for word in temp]
        temp3=[lemmatizer.lemmatize(word=word) for word in temp2]
        data[j]=' '.join(temp3)
    unique_word_count_vectorizer=vectorizer.transform(data)
    return unique_word_count_vectorizer.toarray()
@app.route('/')
def index():
    print("in index",file=sys.stderr)
    return '''
    <form method="POST" action="/saveData">
        <input type="Submit" value="Train the Model">
    </form>
    '''
@app.route('/saveData',methods=["POST"])
def saveData():
    kk=0
    current_id=[]
    for submission in reddit.subreddit('india').top(limit=3):
        kk+=1
        mongo.db.users.insert({'submission_name': "submission_"+str(kk), "author": str(submission.author), "comments": str(submission.comments.list()), "timestamp": submission.created_utc, "body": str(submission.selftext), "id": submission.id, "flair": submission.link_flair_text, "fullName": submission.name, "title": str(submission.title), "upvote_ratio": submission.upvote_ratio, "my_id": '1234'})
    return '''
    <form method="POST" action="/getLabel">
        <input type="text" name="postURL" placeholder"Post's URL">
        <input type="Submit" value="Detect Flair">
    </form>
    '''
@app.route('/getLabel',methods=["POST"])
def getLabel():
    postLink=request.form.get('postURL')
    postID=postLink.split("/")[6]
    post=reddit.submission(id=postID)
    l=[str(post.title),str(post.selftext),str(post.title)+" "+str(post.selftext)]
    newl=[0]*3
    for i in range(len(l)):
        newl[i]=createVector([l[i]],vectorizers[i])
        print(newl[i].shape)
    finalAns=detectFlair(newl)
    print(finalAns)
    return finalAns


if __name__ == '__main__':
   app.run()