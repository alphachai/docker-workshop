from django.forms import ModelForm
from scorekeeper.models import Score

# Create the form class.
class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ['player_one', 'player_two', 'score_one', 'score_two']
