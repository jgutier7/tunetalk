from flask import Flask, request, render_template, redirect, url_for, flash
import openai
import os

# Set up OpenAI API credentials
openai.api_key = "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"

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9176')

