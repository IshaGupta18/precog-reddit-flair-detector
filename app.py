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
reddit=praw.Reddit(client_id=os.environ['CLIENT_ID_REDDIT'], client_secret=os.environ['CLIENT_SECRET_REDDIT'],
                     password=os.environ['PASSWORD_REDDIT'], user_agent='testing praw',
                     username=os.environ['USERNAME_REDDIT'])
app = Flask(__name__,static_folder="templates/static")
app.config['MONGO_URI']=os.environ['MONGODB_URI']
mongo = PyMongo(app)
accuracy1=0
accuracy2=0
accuracy3=0
hash_labels={}
allLabels=[]
reverse_hash_labels={}
temparr=[]
tfidf_model_title, tfidf_model_body, tfidf_model_title_body = TfidfVectorizer(), TfidfVectorizer(), TfidfVectorizer()

def detectFlair(detectData):
    # accuracy1=metrics.accuracy_score(actualLabel, ans1)
    # accuracy2=metrics.accuracy_score(actualLabel, ans2)
    # accuracy3=metrics.accuracy_score(actualLabel, ans3)
    model1=pickle.load(open("./titleModeldump.pkl", "rb"))
    model2=pickle.load(open("./bodyModeldump.pkl", "rb"))
    model3=pickle.load(open("./title_bodyModeldump.pkl", "rb"))
    #print(type(detectData[0]))
    # print(detectData.shape)
    ans1 = model1.predict(detectData[0])
    print(ans1)
    # return reverse_hash_labels[ans1]
    # ans2=model2.predict(detectData[1])
    # ans3=model3.predict(detectData[2])
    # np.unique
    # d={}
    # l=[ans1,ans2,ans3]
    # acc=[accuracy1,accuracy2,accuracy3]
    # for i in range(len(l)):
    #     if l[i] not in d:
    #         d[l[i]]=[0,acc[i],l[i]]
    #     else:
    #         d[l[i]][0]+=1
    # arr=[]
    # for i in d:
    #     arr.append(i)
    # arr.sort(key=lambda x: (-x[0],-x[1]))
    # return reverse_hash_labels[arr[0][2]]

    return reverse_hash_labels[ans1[0]]

    # hahahahaha
def createVector(data):
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
        # print(temp3)
        data[j]=' '.join(temp3)
    # 
    # tfidf_vectorizer=TfidfVectorizer(use_idf=True)
    unique_word_count_vectorizer=tfidf_model_title.transform(data)
    # detectFlair(unique_word_count_vectorizer.toarray(),actualLabel)
    return unique_word_count_vectorizer.toarray()
def preprocessor(data):
    stop_words=set(stopwords.words('english'))
    stemmer=PorterStemmer()
    lemmatizer=WordNetLemmatizer()
    uniquewords={}
    labels=[0]*len(data)
    print("data",len(data))
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
def titleModel(titles):
    titlesProcessed,labels=preprocessor(titles)
    #tfidf_vectorizer=TfidfVectorizer(use_idf=True)
    unique_word_count_vectorizer=tfidf_model_title.fit_transform(titlesProcessed)
    temparr=unique_word_count_vectorizer
    print("temparr",temparr)
    X_train, X_test, Y_train, Y_test = train_test_split(unique_word_count_vectorizer, labels, test_size=0.2,random_state=109)
    mnbTitle = MultinomialNB()
    mnbTitle.fit(X_train.toarray(),Y_train)
    pickle.dump(mnbTitle,open("./titleModeldump.pkl","ab"))
    Y_predicted=mnbTitle.predict(X_test.toarray())
    accuracy1=metrics.accuracy_score(Y_test, Y_predicted)
    # print("Accuracy:",metrics.accuracy_score(Y_test, Y_predicted))
def bodyModel(body):
    bodyProcessed,labels=preprocessor(body)
    #tfidf_vectorizer=TfidfVectorizer(use_idf=True)
    unique_word_count_vectorizer=tfidf_model_body.fit_transform(bodyProcessed)
    X_train, X_test, Y_train, Y_test = train_test_split(unique_word_count_vectorizer, labels, test_size=0.2,random_state=109)
    mnbBody = MultinomialNB()
    mnbBody.fit(X_train.toarray(),Y_train)
    pickle.dump(mnbBody,open("./bodyModeldump.pkl","ab"))
    Y_predicted=mnbBody.predict(X_test.toarray())
    accuracy2=metrics.accuracy_score(Y_test, Y_predicted)
    # Y_predicted=mnbBody.predict(X_test.toarray())
    # print("Accuracy:",metrics.accuracy_score(Y_test, Y_predicted))
def title_bodyModel(title_body):
    title_bodyProcessed,labels=preprocessor(title_body)
    #tfidf_vectorizer=TfidfVectorizer(use_idf=True)
    unique_word_count_vectorizer=tfidf_model_title_body.fit_transform(title_bodyProcessed)
    X_train, X_test, Y_train, Y_test = train_test_split(unique_word_count_vectorizer, labels, test_size=0.2,random_state=109)
    mnbTitleBody = MultinomialNB()
    mnbTitleBody.fit(X_train.toarray(),Y_train)
    pickle.dump(mnbTitleBody,open("./title_bodyModeldump.pkl","ab"))
    Y_predicted=mnbTitleBody.predict(X_test.toarray())
    accuracy3=metrics.accuracy_score(Y_test, Y_predicted)
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
    kk=0
    current_id=[]
    for submission in reddit.subreddit('india').top(limit=1000):
        kk+=1
        # current_id.append()
        mongo.db.users.insert({'submission_name': "submission_"+str(kk), "author": str(submission.author), "comments": str(submission.comments.list()), "timestamp": submission.created_utc, "body": str(submission.selftext), "id": submission.id, "flair": submission.link_flair_text, "fullName": submission.name, "title": str(submission.title), "upvote_ratio": submission.upvote_ratio, "my_id": '1234'})
    print(kk,"the size")
    all_data=mongo.db.users.find({"my_id": '1234'})
    titles=[]
    body=[]
    title_body=[]
    # hash_labels={}
    # allLabels=[]
    t=0
    for i in all_data:
        t+=1
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
    print(len(allLabels))
    for i in hash_labels:
        reverse_hash_labels[hash_labels[i]]=i
    titleModel(titles)
    bodyModel(body)
    title_bodyModel(title_body)
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
    # l=[str(post.title)]
    newl=[0]
    for i in range(len(l)):
        newl[i]=createVector([l[i]])
        print(newl[i].shape)
    # print(newl)
    finalAns=detectFlair(newl)
    print(finalAns)
    return finalAns
    



if __name__ == '__main__':
   app.run(debug=True)