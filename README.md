# precog-reddit-flair-detector
Steps:
1. Fetched Reddit's posts (submissions) using PRAW: Python Reddit API Wrapper
2. Saved the data in a MongoDB instance (local and remote both)
3. Set the project up on a Flask server having 4 Routes:
  index Page: On clicking on "Ready to Go" button, initally, data was being saved in MongoDB instance, but was removed due to its slow speed https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/4824dae2a5258d231f8dd3ecf6b187e2a95943de/app2.py#L81-L85.
  saveData: Would display a form field to paste the link to a Reddit post, and hit submit
  geLabel: Would pass the post to 3 ML models, which will predict an answer and display it.
  stats: Would display some stats about the collected data.
4. ML models:
  Firstly, the collected data was cleaned (title, body, title+body) using NLTK module in Python.
  The cleaned data was then put through a vectorizer, to get a matrix of it.
  This matrix was then split into training and testing data using sklearn.
  A Multinomial distribution was used to train the model.
  The models were then dumped using pickle module and loaded to predict the flair value when user input was received.
  
  https://precog-reddit-flair-detector.herokuapp.com is the Heroku deployment.
  
  MongoDB Dump and code written to set it up: 
  https://github.com/IshaGupta18/precog-reddit-flair-detector/tree/master/mydatabase
  https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/4824dae2a5258d231f8dd3ecf6b187e2a95943de/app2.py#L26-L27
  
  File to run, to view the project locally: python app2.py or python3 app2.py (However, the credentials for the Reddit API haven't been provided, so the user will have to create them and replace them here: https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/e7b6d74ad5c2584c699b85d63902120216e4ef4b/app2.py#L22-L24
 
 ML model files: https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/titleModel.py,
 https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/bodyModel.py, https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/title_bodyModel.py
 
 and their respective dumps: https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/titleModeldump.pkl,
 https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/bodyModeldump.pkl, https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/title_bodyModeldump.pkl
 
 Training and Testing data in CSV format: https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/databaseTest.csv, https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/databaseTrain.csv
 
 Data for brownie points task and the script to collect stats: https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/browniedata.txt, https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/brownie.py, 
 https://github.com/IshaGupta18/precog-reddit-flair-detector/blob/master/dataForAnalysis.py

Templates: https://github.com/IshaGupta18/precog-reddit-flair-detector/tree/master/templates


Resources:

https://praw.readthedocs.io/en/latest/index.html
https://www.tutorialspoint.com/flask
https://flask-pymongo.readthedocs.io/en/latest/
https://github.com/kavgan/nlp-in-practice/blob/master/text-pre-processing/Text%20Preprocessing%20Examples.ipynb
https://medium.com/@datamonsters/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908
http://kavita-ganesan.com/tfidftransformer-tfidfvectorizer-usage-differences/#.XS8qE7ozY5l
https://www.datacamp.com/community/tutorials/naive-bayes-scikit-learn
https://github.com/publiclab/simple-data-grapher: My Google Summer of Code project for UI ideas
Google Sheets: for graphs
