# app.py

from flask import Flask, render_template, redirect, url_for, flash, request
from models import Player, Game
from database import Base, engine, Session  # Import Session from database.py
from forms import AddPlayerForm, AddGameForm
from datetime import datetime
from elo import update_player_ratings


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your own secret key


# Create all tables
Base.metadata.create_all(engine)

@app.teardown_appcontext
def remove_session(exception=None):
    if exception:
        Session.rollback()
    Session.remove()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leaderboard')
def leaderboard():
    players = Session.query(Player).order_by(Player.rating.desc()).all()
    return render_template('leaderboard.html', players=players)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = AddPlayerForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        existing_player = Session.query(Player).filter_by(name=name).first()
        if existing_player:
            flash('Player with this name already exists.', 'danger')
            return redirect(url_for('add_player'))
        new_player = Player(name=name)
        Session.add(new_player)
        Session.commit()
        flash('Player added successfully.', 'success')
        return redirect(url_for('leaderboard'))
    return render_template('add_player.html', form=form)

@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    form = AddGameForm()
    if form.validate_on_submit():
        date = form.date.data
        team1_player_ids = form.team1_players.data
        team2_player_ids = form.team2_players.data
        team1_score = form.team1_score.data
        team2_score = form.team2_score.data

        # Check for overlapping players
        overlapping_players = set(team1_player_ids) & set(team2_player_ids)
        if overlapping_players:
            flash('Players cannot be on both teams.', 'danger')
            return redirect(url_for('add_game'))

        # Retrieve Player objects
        team1_players = Session.query(Player).filter(Player.id.in_(team1_player_ids)).all()
        team2_players = Session.query(Player).filter(Player.id.in_(team2_player_ids)).all()

        # Create Game object
        game = Game(
            date=date,
            team1_score=team1_score,
            team2_score=team2_score,
            team1_players=team1_players,
            team2_players=team2_players
        )
        Session.add(game)

        # Update player ratings
        update_player_ratings(game)

        Session.commit()
        flash('Game added and ratings updated.', 'success')
        return redirect(url_for('leaderboard'))
    return render_template('add_game.html', form=form)

@app.route('/game_history')
def game_history():
    games = Session.query(Game).order_by(Game.date.desc()).all()
    return render_template('game_history.html', games=games)
    
def recalculate_ratings():
    # Reset all player ratings to default
    players = Session.query(Player).all()
    for player in players:
        player.rating = 1000

    Session.commit()

    # Retrieve all games in chronological order
    games = Session.query(Game).order_by(Game.date).all()

    for game in games:
        # Update player ratings for each game
        update_player_ratings(game)

    Session.commit()
   
@app.route('/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    game_to_delete = Session.query(Game).get(game_id)
    if not game_to_delete:
        flash('Game not found.', 'danger')
        return redirect(url_for('game_history'))

    # Delete the game
    Session.delete(game_to_delete)
    Session.commit()

    # Recalculate player ratings
    recalculate_ratings()

    flash('Game removed and ratings recalculated.', 'success')
    return redirect(url_for('game_history'))

@app.context_processor
def inject_now():
    return {'datetime': datetime}

if __name__ == '__main__':
    app.run(debug=True)
