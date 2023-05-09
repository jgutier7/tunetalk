from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import openai
import os
from db_manager import db_session
from flask_bootstrap import Bootstrap
from talk_classes import User, Song

from sqlalchemy.dialects import sqlite
# Set up OpenAI API credentials
# openai.api_key = "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"
openai.api_key = "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"
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'i_hate_this_project_fr'

# Initialize LoginManager
login_manager = LoginManager()

# Configure LoginManager
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Decorator function
from functools import wraps

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db_session.query(User).filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        song = request.form.get('song')
        artist = request.form.get('artist')
        prompt_option = request.form.get('prompt_option')
        session['prompt_option'] = prompt_option  # Store the prompt_option in the session

        character_assumption, error = ai_prompt(song, artist, prompt_option)
        if error:
            flash(f"Error: {error}")
            return redirect(url_for('index'))

        return render_template('index.html', character_assumption=character_assumption)

    return render_template('index.html', character_assumption=None)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = db_session.query(User).filter_by(username=username).first()

        if existing_user is None:
            user = User(username, password)
            db_session.add(user)
            db_session.commit()
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Username already exists')
            return redirect(url_for('signup'))

    return render_template('signup.html')

# Fix the store_songs route
@app.route('/api/store_songs', methods=['POST'])
@login_required
def store_songs():
    songs = request.get_json(force=True)
    stored_songs = []

    current_user_id = db_session.query(User).filter_by(username=session['username']).first().id

    for song in songs:
        song_obj = Song(title=song['title'], artist=song['artist'])
        db_session.add(song_obj)
        db_session.commit()
        stored_songs.append(song_obj)

    openai_function(stored_songs)
    return jsonify(status='success', message='Songs stored successfully')

def ai_prompt(song, artist, prompt_option):
    try:
        prompts = {
            '0': f"If someone recommends the song '{song}' by {artist}, what assumptions can be made about their character?",
            '1': f"Create a short story where the song '{song}' by {artist} is the theme song.",
            '2': f"Imagine '{song}' by {artist} as the soundtrack to a movie scene. Describe that scene in detail.",
            '3': f"Write a fictional conversation between {artist} and another artist, discussing the creation of '{song}'.",
            '4': f"If '{song}' by {artist} were a person, what kind of personality and appearance would they have?",
            '5': f"Create a playlist of 5 songs that would go well with '{song}' by {artist}. Explain why you chose each song.",
            '6': f"Write a poem inspired by the emotions or story conveyed in '{song}' by {artist}.",
            '7': f"Design a new album cover for {artist}'s album that features '{song}'. Describe the visual elements and the concept behind it.",
            '8': f"If '{song}' by {artist} were a dish, what ingredients and flavors would it have? Describe the dish in detail.",
            '9': f"Imagine '{song}' by {artist} as a character in a video game. What abilities, traits, and backstory would they have?",
            '10': f"Describe a dream music festival lineup where {artist} is performing '{song}', along with four other artists/bands. Explain why you chose each artist/band and how they complement each other."
        }

        prompt = prompts.get(prompt_option)
        if not prompt:
            prompt = f"If someone recommends the song '{song}' by {artist}, what assumptions can be made about their character?"

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5,
        )

        character_assumption = response.choices[0].text.strip()
        return character_assumption, None
    except Exception as e:
        return None, str(e)


# def recommend_character_assumption(song, artist):
#     try:
#         ''' prompt = f"If someone recommends the song '{song}' by {artist}, what assumptions can be made about their character? Write me a list of 3 songs that you'd recommend. Then say something passive aggressive about the song or the artist."
# '''
#         prompt = f"If someone recommends the song '{song}' by {artist}, what assumptions can be made about their character?"
#         response = openai.Completion.create(
#             engine="text-davinci-002",
#             prompt=prompt,
#             max_tokens=50,
#             n=1,
#             stop=None,
#             temperature=0.5,
#         )

#         character_assumption = response.choices[0].text.strip()
#         return character_assumption, None
#     except Exception as e:
#         return None, str(e)

from spotify_auth import spotify_client
@app.route('/spotify/callback')
def spotify_callback():
    # You can access the user's data using the `spotify_client` object
    # o get the currently playing track,
    current_track = spotify_client.current_playback()
    print(f"Session username: {session['username']}")
    query = db_session.query(User).filter_by(username=session['username'])
    
    # Print the SQL query and its parameters
    compiled_query = query.statement.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True})
    print(f"SQL Query: {compiled_query}")
    
    user = query.first()
    if not user:
        flash("Error: User not found")
        return redirect(url_for('index'))

    current_user_id = user.id
    # Store the current_track in the songs table
    current_user_id = db_session.query(User).filter_by(username=session['username']).first().id
    prompt_option = session.get('prompt_option', None)  # Retrieve the stored prompt_option from the session
    song_obj = Song(title=current_track['item']['name'], artist=current_track['item']['artists'][0]['name'], user_id=current_user_id, prompt_option = prompt_option)
    db_session.add(song_obj)
    db_session.commit()

    # Send the stored song to the OpenAI query
    # prompt_option = session.get('prompt_option', None)  # Retrieve the stored prompt_option from the session
    # ^^ weird bug occuring, ditching the prompt option 
    character_assumption, error = ai_prompt(song_obj.title, song_obj.artist, prompt_option)
    if error:
        flash(f"Error: {error}")
        return redirect(url_for('index'))

    return render_template('index.html', character_assumption=character_assumption)

@app.route('/spotify_assumption')
@login_required
def spotify_assumption():
    current_user_id = db_session.query(User).filter_by(username=session['username']).first().id
    last_song = db_session.query(Song).filter_by(user_id=current_user_id).order_by(Song.id.desc()).first()

    if last_song:
        song = last_song.title
        artist = last_song.artist
        album_cover = last_song.image_url  # Get the album cover URL from the Song object
        character_assumption, error = ai_prompt(song, artist, prompt_option='0')
    else:
        song = None
        artist = None
        album_cover = None
        character_assumption = None

    return render_template('spotify_assumption.html', song=song, artist=artist, album_cover=album_cover, character_assumption=character_assumption, prompt = '0')

# @app.route('/spotify_assumption')
# @login_required
# def spotify_assumption():
#     current_user_id = db_session.query(User).filter_by(username=session['username']).first().id
#     last_song = db_session.query(Song).filter_by(user_id=current_user_id).order_by(Song.id.desc()).first()

#     if last_song:
#         song = last_song.title
#         artist = last_song.artist
#         album_cover = last_song.image_url  # Get the album cover URL from the Song object
#         prompt_option = last_song.prompt_option  # Get the prompt option from the Song object
#         character_assumption, error = ai_prompt(song, artist, prompt_option)
#     else:
#         song = None
#         artist = None
#         album_cover = None
#         character_assumption = None

#     return render_template('spotify_assumption.html', song=song, artist=artist, album_cover=album_cover, character_assumption=character_assumption)


@app.route('/spotify/auth')
def spotify_auth():
    auth_url = spotify_client.auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9152')

