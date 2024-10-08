# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, IntegerField, SubmitField, DateField, widgets
from wtforms.validators import DataRequired, InputRequired, NumberRange
from models import Player
from database import Session  # Import Session

class AddPlayerForm(FlaskForm):
    name = StringField('Player Name', validators=[DataRequired()])
    submit = SubmitField('Add Player')

class AddGameForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    team1_players = SelectMultipleField(
        'Team 1 Players',
        coerce=int,
        choices=[],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )
    team2_players = SelectMultipleField(
        'Team 2 Players',
        coerce=int,
        choices=[],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )
    team1_score = IntegerField('Team 1 Score', validators=[InputRequired(), NumberRange(min=0)])
    team2_score = IntegerField('Team 2 Score', validators=[InputRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(AddGameForm, self).__init__(*args, **kwargs)
        # Populate player choices
        players = Session.query(Player).order_by(Player.name).all()
        choices = [(player.id, player.name) for player in players]
        self.team1_players.choices = choices
        self.team2_players.choices = choices
