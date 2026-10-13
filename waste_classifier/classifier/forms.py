from django import forms
from .models import COLORS, MODEL_CHOICES, SHAPES, TEXTURES, _choices


class PredictForm(forms.Form):
    weight = forms.FloatField(label="Weight (grams)", min_value=0.1)
    size = forms.FloatField(label="Size (cm, longest side)", min_value=0.1)
    shape = forms.ChoiceField(choices=_choices(SHAPES))
    texture = forms.ChoiceField(choices=_choices(TEXTURES))
    color = forms.ChoiceField(choices=_choices(COLORS))
    model_used = forms.ChoiceField(label="Algorithm", choices=MODEL_CHOICES, initial="random_forest")
