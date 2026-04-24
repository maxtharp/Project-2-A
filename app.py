from flask import Flask, flash, redirect, render_template, request, url_for
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-only-key'

games = [
    {'id': 1, 'title': 'Tekken 5', 'genre': 'Fighting', 'release_year': 2004, 'notes': 'Arcade classic'},
    {'id': 2, 'title': 'Metal Gear Solid 3', 'genre': 'Action-Adventure', 'release_year': 2004, 'notes': 'Stealth masterpiece'},
    {'id': 3, 'title': 'Resident Evil 4', 'genre': 'Survival Horror', 'release_year': 2005, 'notes': 'Great pacing'},
    {'id': 4, 'title': 'Dark Souls 2', 'genre': 'Action RPG', 'release_year': 2014, 'notes': 'Challenging combat'},
]


def _validate_text(value: str, field_name: str) -> str | None:
    if not value:
        return f'{field_name} is required.'
    if len(value) > 100:
        return f'{field_name} must be 100 characters or fewer.'
    return None


def _next_id() -> int:
    if not games:
        return 1
    return max(item['id'] for item in games) + 1

@app.route("/")
def home():
    return render_template('best_games.html', games=games)


@app.post('/add')
def add_game():
    title = request.form.get('title', '').strip()
    genre = request.form.get('genre', '').strip()
    notes = request.form.get('notes', '').strip()
    release_year_raw = request.form.get('release_year', '').strip()

    errors = [
        _validate_text(title, 'Title'),
        _validate_text(genre, 'Genre'),
        _validate_text(notes, 'Notes'),
    ]
    errors = [error for error in errors if error]

    try:
        release_year = int(release_year_raw)
        if release_year < 1970 or release_year > 2100:
            errors.append('Release year must be between 1970 and 2100.')
    except ValueError:
        errors.append('Release year must be a valid integer.')

    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('home'))

    games.append(
        {
            'id': _next_id(),
            'title': title,
            'genre': genre,
            'notes': notes,
            'release_year': release_year,
        }
    )
    flash('Game added.', 'success')
    return redirect(url_for('home'))


@app.post('/delete/<int:game_id>')
def delete_game(game_id: int):
    for idx, item in enumerate(games):
        if item['id'] == game_id:
            del games[idx]
            flash('Game deleted.', 'success')
            break
    else:
        flash('Game not found.', 'warning')

    return redirect(url_for('home'))

