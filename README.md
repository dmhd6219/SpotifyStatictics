# Spotify Music Profile Statistics Web App

![License](https://img.shields.io/github/license/dmhd6219/SpotifyStatictics)
![Python](https://img.shields.io/badge/python-blue)
![Flask](https://img.shields.io/badge/flask-orange)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

This repository contains a web application built on Flask that allows users to log in using their Spotify accounts and
view their music profile statistics. The app was created with the idea of sharing beautiful music profiles, enabling
users to explore their music listening habits and statistics in an aesthetically pleasing manner.

## Features

- User authentication through Spotify accounts
- View personalized music statistics
- Attractive visualizations to present the data in an engaging manner
- Easy sharing options to showcase music profiles with friends and social networks

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/dmhd6219/SpotifyStatictics.git
```

2. Create a virtual environment and activate it (optional but recommended):

```bash
cd SpotifyStatictics
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

To run the web application, you will need to set up a Spotify Developer account and obtain the necessary API
credentials. Follow these steps:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in with your Spotify
   account.
2. Create a new application and note down the `Client ID` and `Client Secret`.
3. In the project directory, create a new file named `.env` and add the following lines:

```env
SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback'  # Change this if required
```

Replace `your_spotify_client_id` and `your_spotify_client_secret` with the credentials obtained in step 2.

## Usage

1. Run the Flask development server:

```bash
python app.py
```

2. Open your web browser and go to `http://localhost:8080`.

3. Click on the "Login with Spotify" button to authenticate using your Spotify account.

4. Once logged in, you'll be able to explore your music profile statistics and visualize your music preferences.

## Deployment

To deploy the web app for public use, consider using platforms like Heroku, AWS, or others that support Flask
applications.

## Contributing

Contributions are welcome! If you want to add new features, fix bugs, or improve the existing codebase, feel free to
open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy exploring and sharing your music profile statistics with the world! 🎶📊

# Screenshots

![Profile page](/screenshots/Screenshot_1.png)
![Statistics page](/screenshots/Screenshot_2.png)