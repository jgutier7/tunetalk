Tunetalk: A Programming Paradigms Project

Tunetalk is a web-based application designed to demonstrate the application of various programming paradigms and concepts learned in class. By leveraging the power of the OpenAI API and the Spotify API, Tunetalk enables users to generate creative content based on their favorite songs and artists. The project showcases the use of object-oriented, functional, and event-driven programming techniques to create a seamless, engaging, and user-friendly experience.

Features
User authentication and registration
Creative content generation using OpenAI API
Integration with the Spotify API for user's currently playing song
Customizable creative prompts
Responsive and user-friendly design
Programming Paradigms

Object-Oriented Programming (OOP)
Tunetalk utilizes object-oriented programming principles to create a well-structured, modular, and maintainable codebase. Classes, inheritance, and encapsulation are employed to define and organize the application's data models and their associated methods. For example, the User and Song classes in the project represent the users and their submitted songs, respectively.

Functional Programming (FP)
Functional programming concepts, such as higher-order functions, immutability, and pure functions, are used throughout Tunetalk to create clean, efficient, and easily testable code. For instance, the use of Python's built-in higher-order functions, such as map() and filter(), helps to process and transform data in a concise and readable manner.

Event-Driven Programming (EDP)
The project leverages event-driven programming techniques to handle user interactions and manage application state. The Flask web framework's routing and event handling system allows the application to respond to user requests and update the UI accordingly. This enables a dynamic and interactive experience for users, as the application can react to their actions in real-time.

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
