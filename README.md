Tunetalk: A Programming Paradigms Project

Tunetalk is a web-based application designed to demonstrate the application of various programming paradigms and concepts learned in class. By leveraging the power of the OpenAI API and the Spotify API, Tunetalk enables users to generate creative content based on their favorite songs and artists. The project showcases the use of object-oriented, functional, and event-driven programming techniques to create a seamless, engaging, and user-friendly experience.

Features
User authentication and registration
Creative content generation using OpenAI API
Integration with the Spotify API for user's currently playing song
Customizable creative prompts
Responsive and user-friendly design

Getting Started

To set up and run Tunetalk locally
Clone the repo
Set up your environment variables for the OpenAI API key and the Spotify API credentials. You can create a .env file and include the following variables:
makefile. I have my keys in there currently (they don't work anymore)
OPENAI_API_KEY=your_openai_api_key
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=your_spotify_redirect_uri
Run the application:
python3 talk.py
