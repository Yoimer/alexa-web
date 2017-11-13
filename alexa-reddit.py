from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

# get headlines from reddit 
def get_headlines():
	
	# log into reddit
    user_pass_dict = {'user': 'Yoimer-David',
                      'passwd': 'nextwells',
                      'api_type': 'json'}
                      
    sess = requests.Session()
    
    sess.headers.update({'User-Agent': 'I am testing Alexa: Sentdex'})
    
    # go to subreddit
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    
    time.sleep(1)
    
    url = 'https://reddit.com/r/worldnews/.json?limit=10'
    
    html = sess.get(url)
    
    # get data from subreddit
    data = json.loads(html.content.decode('utf-8'))
    
    # just get titles from data
    titles = []
    for listing in data['data']['children']:
        title = unidecode.unidecode(listing['data']['title'])
        titles.append(title)
    titles = '... '.join([i for i in titles])
    
    return titles

@app.route('/')
def homepage():
    return "hi there, how ya doin?"

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like the news?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current world news headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)
    
if __name__ == '__main__':
    app.run(debug=True)
