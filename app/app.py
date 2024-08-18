from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample game data for demonstration purposes
games = [
    {'title': 'The Witcher 3', 'genre': 'RPG', 'platform': 'PC', 'cover': 'witcher3.jpg'},
    {'title': 'Cyberpunk 2077', 'genre': 'RPG', 'platform': 'PC', 'cover': 'cyberpunk2077.jpg'},
    {'title': 'Super Mario Odyssey', 'genre': 'Platformer', 'platform': 'Nintendo Switch', 'cover': 'mario.jpg'}
]

@app.route('/')
def home():
    return render_template('index.html', games=games)

@app.route('/game/<string:title>')
def game_details(title):
    game = next((game for game in games if game['title'] == title), None)
    if game:
        return render_template('game_details.html', game=game)
    else:
        return 'Game not found', 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
