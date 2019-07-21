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
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
reddit=praw.Reddit(client_id="GXSJ2q3iO6H1sw", client_secret="4HcvsdQ14CZMKRp1__ZkjkRnXGE",
                     password="ishagupta18", user_agent='testing praw',
                     username="isha_gupta18")
app = Flask(__name__)
app.config['MONGO_URI']="mongodb://gdgnd:gdgnd19@ds119755.mlab.com:19755/gdgndnodeangular"
mongo = PyMongo(app)
def preprocessor(data,hash_labels,allLabels):
    stop_words=set(stopwords.words('english'))
    stemmer=PorterStemmer()
    lemmatizer=WordNetLemmatizer()
    uniquewords={}
    labels=[0]*len(data)
    for j in range(len(data)):
        labels[j]=hash_labels[allLabels[j]]
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
        for word in temp3:
            if word in uniquewords:
                uniquewords[word]+=1
            else:
                uniquewords[word]=1
    return data,labels
def titleModel(titles,hash_labels,allLabels):
    titlesProcessed,labels=preprocessor(titles,hash_labels,allLabels)
    tfidf_vectorizer=TfidfVectorizer(use_idf=True)
    unique_word_count_vectorizer=tfidf_vectorizer.fit_transform(titlesProcessed)
    X_train, X_test, Y_train, Y_test = train_test_split(unique_word_count_vectorizer, labels, test_size=0.2,random_state=109)
    mnbTitle = MultinomialNB()
    mnbTitle.fit(X_train.toarray(),Y_train)
    # Y_predicted=mnbTitle.predict(X_test.toarray())
    # print("Accuracy:",metrics.accuracy_score(Y_test, Y_predicted))
def bodyModel(body,hash_labels,allLabels):
    bodyProcessed,labels=preprocessor(body,hash_labels,allLabels)
    tfidf_vectorizer=TfidfVectorizer(use_idf=True)
    unique_word_count_vectorizer=tfidf_vectorizer.fit_transform(bodyProcessed)
    X_train, X_test, Y_train, Y_test = train_test_split(unique_word_count_vectorizer, labels, test_size=0.2,random_state=109)
    mnbBody = MultinomialNB()
    mnbBody.fit(X_train.toarray(),Y_train)
    # Y_predicted=mnbBody.predict(X_test.toarray())
    # print("Accuracy:",metrics.accuracy_score(Y_test, Y_predicted))
def title_bodyModel(title_body,hash_labels,allLabels):
    title_bodyProcessed,labels=preprocessor(title_body,hash_labels,allLabels)
    tfidf_vectorizer=TfidfVectorizer(use_idf=True)
    unique_word_count_vectorizer=tfidf_vectorizer.fit_transform(title_bodyProcessed)
    X_train, X_test, Y_train, Y_test = train_test_split(unique_word_count_vectorizer, labels, test_size=0.2,random_state=109)
    mnbTitleBody = MultinomialNB()
    mnbTitleBody.fit(X_train.toarray(),Y_train)
    # Y_predicted=mnbTitleBody.predict(X_test.toarray())
    # print("Accuracy:",metrics.accuracy_score(Y_test, Y_predicted))
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
    i=0
    for submission in reddit.subreddit('india').top(limit=3):
        i+=1
        mongo.db.users.insert({'submission_name': "submission_"+str(i), "author": str(submission.author), "comments": str(submission.comments.list()), "timestamp": submission.created_utc, "body": submission.selftext, "id": submission.id, "flair": submission.link_flair_text, "fullName": submission.name, "title": submission.title, "upvote_ratio": submission.upvote_ratio})
    all_data=mongo.db.users.find()
    titles=[]
    body=[]
    title_body=[]
    hash_labels={}
    allLabels=[]
    for i in all_data:
        titles.append(i["title"])
        body.append(i["body"])
        title_body.append(i["title"]+" "+i["body"])
        allLabels.append(i["flair"])
        try:
            if hash_labels[i["flair"]]==0:
                pass
        except:
            hash_labels[i["flair"]]=0
        tempCounter=0
        for j in hash_labels:
            hash_labels[j]=tempCounter
            tempCounter+=1
    titleModel(titles,hash_labels,allLabels)
    bodyModel(body,hash_labels,allLabels )
    title_bodyModel(title_body,hash_labels,allLabels)
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
    



if __name__ == '__main__':
   app.run()