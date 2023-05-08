from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import openai
import os
from db_manager import db_session
from flask_bootstrap import Bootstrap
from talk_classes import User, Song


from spotify_auth import app, auth_query_parameters, SPOTIFY_AUTH_URL, SPOTIFY_TOKEN_URL, SPOTIFY_API_URL

# Modify the /spotify/auth route
@app.route('/spotify/auth')
def spotify_auth():
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

# Replace the spotify_callback() function
@app.route('/spotify/callback')
def spotify_callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    display_arr = [profile_data] + playlist_data["items"]
    return render_template("index.html", sorted_array=display_arr)


# Set up OpenAI API credentials
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

        if not song or not artist:
            flash("Both song and artist must be provided")
            return redirect(url_for('index'))

        character_assumption, error = recommend_character_assumption(song, artist)
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

def recommend_character_assumption(song, artist):
    try:
        ''' prompt = f"If someone recommends the song '{song}' by {artist}, what assumptions can be made about their character? Write me a list of 3 songs that you'd recommend. Then say something passive aggressive about the song or the artist."
'''
        prompt = f"If someone recommends the song '{song}' by {artist}, what assumptions can be made about their character?"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )

        character_assumption = response.choices[0].text.strip()
        return character_assumption, None
    except Exception as e:
        return None, str(e)


@app.route('/spotify/callback')
def spotify_callback():
    # This code will be executed after a user authorizes your app
    # You can access the user's data using the `spotify_client` object
    # For example, to get the currently playing track, you can call the following function:
    current_track = spotify_client.current_playback()
    
    # Store the current_track in the songs table
    current_user_id = db_session.query(User).filter_by(username=session['username']).first().id
    song_obj = Song(title=current_track['item']['name'], artist=current_track['item']['artists'][0]['name'], user_id=current_user_id)
    db_session.add(song_obj)
    db_session.commit()

    # Send the stored song to the OpenAI query
    character_assumption, error = recommend_character_assumption(song_obj.title, song_obj.artist)
    if error:
        flash(f"Error: {error}")
        return redirect(url_for('index'))

    return render_template('index.html', character_assumption=character_assumption)


# @app.route('/spotify/callback')
# def spotify_callback():
#     code = request.args.get('code')
#     if not code:
#         error = request.args.get('error')
#         if error:
#             flash(f"Spotify login error: {error}")
#         else:
#             flash("Spotify login error: missing code")
#         return redirect(url_for('index'))

#     try:
#         token_info = spotify_client.auth_manager.get_access_token(code)
#         spotify_client.auth_manager._token_info = token_info

#         current_track = spotify_client.current_playback()
#         current_user_id = db_session.query(User).filter_by(username=session['username']).first().id
#         album_cover_url = current_track['item']['album']['images'][0]['url']  # Get the album cover URL

#         song_obj = Song(
#             title=current_track['item']['name'],
#             artist=current_track['item']['artists'][0]['name'],
#             user_id=current_user_id,
#             image_url=album_cover_url  # Add this line
#         )
        
#         db_session.add(song_obj)
#         db_session.commit()

#     except Exception as e:
#         flash(f"Error: {str(e)}")
#         return redirect(url_for('index'))

    # character_assumption, error = recommend_character_assumption(song_obj.title, song_obj.artist)
    # if error:
    #     flash(f"Error: {error}")
    #     return redirect(url_for('index'))

    return redirect(url_for('spotify_assumption'))  # Redirect to the new page instead of rendering the index

@app.route('/spotify_assumption')
@login_required
def spotify_assumption():
    current_user_id = db_session.query(User).filter_by(username=session['username']).first().id
    last_song = db_session.query(Song).filter_by(user_id=current_user_id).order_by(Song.id.desc()).first()

    if last_song:
        song = last_song.title
        artist = last_song.artist
        album_cover = last_song.image_url  # Get the album cover URL from the Song object
        character_assumption, error = recommend_character_assumption(song, artist)
    else:
        song = None
        artist = None
        album_cover = None
        character_assumption = None

    return render_template('spotify_assumption.html', song=song, artist=artist, album_cover=album_cover, character_assumption=character_assumption)

@app.route('/spotify/auth')
def spotify_auth():
    auth_url = spotify_client.auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9152')

