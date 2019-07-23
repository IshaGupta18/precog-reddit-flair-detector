import praw
import re
import string
import os
filehandle=open("database.txt","w")
reddit=praw.Reddit(client_id=os.environ['CLIENT_ID_REDDIT'], client_secret=os.environ['CLIENT_SECRET_REDDIT'],
                     password=os.environ['PASSWORD_REDDIT'], user_agent='testing praw',
                     username=os.environ['USERNAME_REDDIT'])
actualLabels={'AMA':0,'AskIndia':0,'Business/Finance':0,'Entertainment':0,'Food':0,'Lifehacks':0,'Non-Political':0,'Photography':0,'Policy/Economy':0,'Politics':0,'Science/Technology':0,'Sports':0,'[R]eddiquette':0}
for submission in reddit.subreddit('india').top(limit=1000):
    if submission.link_flair_text not in actualLabels:
        continue
    filehandle.write(str(submission.link_flair_text)+","+str(submission.score)+","+str(submission.num_comments)+","+str(submission.created_utc)+","+str(submission.upvote_ratio)+","+str(submission.author)+","+str(submission.selftext.encode('utf-8').strip())+","+str(submission.id.encode('utf-8').strip())+","+str(submission.name.encode('utf-8').strip())+","+str(submission.title.encode('utf-8').strip())+"\n")
filehandle.close()