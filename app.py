from flask import Flask, render_template
app = Flask(__name__)

games = [
    {'id': 1, 'name': "Tekken 5", 'photo': "tekken.jpg"},
    {'id': 2, 'name': "Metal Gear Solid 3", 'photo': "metal_gear.jpg"},
    {'id': 3, 'name': "Resident Evil 4", 'photo': "resident_evil.jpg"},
    {'id': 4, 'name': "Dark Souls 2", 'photo': "dark_souls.jpg"},
]

@app.route("/")
def home():
    return render_template('best_games.html', games=games)

