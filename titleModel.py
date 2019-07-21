import praw
import re
import string
import nltk
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
reddit=praw.Reddit(client_id=os.environ['CLIENT_ID_REDDIT'], client_secret=os.environ['CLIENT_SECRET_REDDIT'],
                     password=os.environ['PASSWORD_REDDIT'], user_agent='testing praw',
                     username=os.environ['USERNAME_REDDIT'])


titles=[]
hash_labels={}
labelsTrain=[]
testTitles=[]
testLabels=[]
i=0
for submission in reddit.subreddit('india').top(limit=1000):
    i+=1
    titles.append(submission.title)
    labelsTrain.append(submission.link_flair_text)
    try:
        if hash_labels[submission.link_flair_text]==0:
            pass
    except:
        hash_labels[submission.link_flair_text]=0
print(i)
tempCounter=0
for j in hash_labels:
    hash_labels[j]=tempCounter
    tempCounter+=1
stop_words=set(stopwords.words('english'))
stemmer=PorterStemmer()
lemmatizer=WordNetLemmatizer()
uniquewords={}
labels=[0]*len(titles)
for j in range(len(titles)):
    labels[j]=hash_labels[labelsTrain[j]]
    temp=titles[j].lower()
    temp=re.sub(r'\d+', '', temp)
    # temp=temp.translate(string.maketrans("","",string.punctuation))
    # temp=temp.translate(None,string.punctuation)
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
    titles[j]=' '.join(temp3)
    for word in temp3:
        if word in uniquewords:
            uniquewords[word]+=1
        else:
            uniquewords[word]=1
# uniquewords=sorted(uniquewords.items(), key=lambda x: x[1], reverse=True)
# print(uniquewords)
tfidf_vectorizer=TfidfVectorizer(use_idf=True)
unique_word_count_vectorizer=tfidf_vectorizer.fit_transform(titles)
X_train, X_test, Y_train, Y_test = train_test_split(unique_word_count_vectorizer, labels, test_size=0.2,random_state=109)
gnb = MultinomialNB()
gnb.fit(X_train.toarray(),Y_train)
Y_predicted=gnb.predict(X_test.toarray())
print("Accuracy:",metrics.accuracy_score(Y_test, Y_predicted))