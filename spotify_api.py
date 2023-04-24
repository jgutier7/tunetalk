#!/usr/bin/env python3

''' reddit_api.py -- Jacob Gutierrez '''

from flask import Flask ,request
from flask_sqlalchemy import SQLAlchemy
from db_manager import db_session
from reddit_classes import Settings, Subreddit, Post

app = Flask(__name__)

setr = None
subs = None

def check_globals() -> None: # 8 LOC
    global setr
    global subs

    # create the settings object if it doesn't exist
    # if not setr:
    #     setr = db_session.query(Settings).first()
    if not setr:
        setr = db_session.query(Settings).first()
        
        if not setr: 
            setr = Settings()
            db_session.add(setr)
            db_session.commit()

    # get the subreddit objects from the database and add the settings object
    # if the subreddit objects don't already exist
    if not subs:
        subs = db_session.query(Subreddit).all()
        # for sub in subs:
        #     if setr not in sub.settings: 
        #         sub.settings.append(setr)
    db_session.commit()


@app.route('/')
def display_subreddits() -> str: # 6 LOC
    check_globals() 

    # return a string containing all of the subreddit links
    links = [f'<a href="{sub.url}">[{sub.id}]: {sub.url}</a>' for sub in subs] # hyperlinks the actual text thats displayed 
    return '<br>'.join(links) # joins the links with a line break and retirns it


@app.route('/<int:sub_id>/')
def display_post_titles(sub_id: int) -> str: # 2 LOC
    check_globals()
    # return a string containing all of the titles for the subreddit specified
    # query the database to get the Subreddit object with the given id
    subreddit = db_session.query(Subreddit).get(sub_id) 
    # uuse the display() method of the Subreddit object to get the post titles
    titles = subreddit.display(loc=sub_id, titles=True)
    return titles


@app.route('/<int:sub_id>/<int:post_id>/')
def display_post_comments(sub_id: int, post_id: int) -> str: # 6 LOC
    check_globals()
    # return a string containing all of the comments for the subreddit and post specified
    # Query the database to get the Post object with the given id
    post = db_session.query(Post).get(post_id)
    # Use the display_comment_tre method of the post object to get the post title and comment tree
    comment_tree = post.display_comment_tree(loc=post_id, reply_dict={},depth=setr.comment_num)   
    
    return comment_tree

@app.route('/settings/', methods=['POST'])
def settings() -> None: # 12 LOC
    global settings_dict

    # update the Settings object with the new items from the POST request JSON
    json_data = request.json
    if not json_data:
        return "No JSON data", 400
    for key in json_data:
        settings_dict[key] = json_data[key]
    
    # return a status code for a successful POST request
    return "SUCCESS", 200

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
