import praw
import re
import string
# import pandas as pd
import nltk
import pickle
import os
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
# from sklearn.externals import joblib
reddit=praw.Reddit(client_id=os.environ['CLIENT_ID_REDDIT'], client_secret=os.environ['CLIENT_SECRET_REDDIT'],
                     password=os.environ['PASSWORD_REDDIT'], user_agent='testing praw',
                     username=os.environ['USERNAME_REDDIT'])
actualLabels={'AMA':0,'AskIndia':0,'Business/Finance':0,'Entertainment':0,'Food':0,'Lifehacks':0,'Non-Political':0,'Photography':0,'Policy/Economy':0,'Politics':0,'Science/Technology':0,'Sports':0,'[R]eddiquette':0}
titles=[]
hash_labels={}
reverse_hash_labels={}
labelsTrain=[]
testTitles=[]
testLabels=[]
flairs=[]
i=0
for submission in reddit.subreddit('india').top(limit=1000):
    if submission.link_flair_text not in actualLabels:
        continue
    if "http" in submission.selftext:
        continue
    i+=1
    titles.append(submission.selftext)
    labelsTrain.append(submission.link_flair_text)
    if submission.link_flair_text not in flairs:
        flairs.append(submission.link_flair_text)
flairs.sort()
tempCounter=0
for j in flairs:
    hash_labels[j]=tempCounter
    tempCounter+=1
for j in hash_labels:
    reverse_hash_labels[hash_labels[j]]=j
stop_words=set(stopwords.words('english'))
stemmer=PorterStemmer()
lemmatizer=WordNetLemmatizer()
uniquewords={}
labels=[0]*len(titles)
for j in range(len(titles)):
    labels[j]=hash_labels[labelsTrain[j]]
    temp=titles[j].lower()
    temp=re.sub(r'\d+', '', temp)
    tempstr=""
    for char in temp:
        if char not in string.punctuation:
            tempstr+=char
    temp=tempstr
    temp=temp.strip()
    temp=temp.replace('\n', ' ')
    t=word_tokenize(temp)
    temp=[k for k in t if not k in stop_words]
    temp2=[stemmer.stem(word=word) for word in temp]
    temp3=[lemmatizer.lemmatize(word=word) for word in temp2]
    titles[j]=' '.join(temp3)
    for word in temp3:
        if word in uniquewords:
            uniquewords[word]+=1
        else:
            uniquewords[word]=1
tfidf_vectorizer=TfidfVectorizer(use_idf=True)
unique_word_count_vectorizer=tfidf_vectorizer.fit_transform(titles)
X_train, X_test, Y_train, Y_test = train_test_split(unique_word_count_vectorizer, labels, test_size=0.2,random_state=109)
gnb = MultinomialNB()
gnb.fit(X_train.toarray(),Y_train)
Y_predicted=gnb.predict(X_test.toarray())
a=metrics.accuracy_score(Y_test, Y_predicted)
# joblib.dump(gnb, "./bodyModeldump.pkl")
# joblib.dump(tfidf_vectorizer,"./x2.pkl")
pickle.dump(gnb,open("./bodyModeldump.pkl","wb"))
pickle.dump([tfidf_vectorizer,a,reverse_hash_labels],open("./body.bin","wb"))
print("Accuracy:",metrics.accuracy_score(Y_test, Y_predicted))