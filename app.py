from flask import Flask, request, url_for
from flask_pymongo import PyMongo
import pymongo
import praw
import os
reddit=praw.Reddit(client_id=os.environ['CLIENT_ID_REDDIT'], client_secret=os.environ['CLIENT_SECRET_REDDIT'],
                     password=os.environ['PASSWORD_REDDIT'], user_agent='testing praw',
                     username=os.environ['USERNAME_REDDIT'])
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
databaseAll = myclient["mydatabase"]
app = Flask(__name__)
app.config['MONGO_URI']="mongodb://gdgnd:gdgnd19@ds119755.mlab.com:19755/gdgndnodeangular"
# mongodb://gdgnd:gdgnd19@ds119755.mlab.com:19755/gdgndnodeangular
mongo = PyMongo(app)
@app.route('/')
def index():
    i=0
    for submission in reddit.subreddit('india').hot(limit=10):
        i+=1
        mongo.db.users.insert({'submission_name': "submission_"+str(i), "author": str(submission.author), "comments": str(submission.comments.list()), "timestamp": submission.created_utc, "body": submission.selftext, "id": submission.id, "flair": submission.link_flair_text, "fullName": submission.name, "title": submission.title, "upvote_ratio": submission.upvote_ratio})
    return '''
    <form method="POST" action="/saveData">
        <input type="text" placeholder="Post's URL">
        <input type="Submit">
    </form>
    '''
@app.route('/saveData',methods=["POST"])
def saveData():
    
    return 'Done'



if __name__ == '__main__':
   app.run()