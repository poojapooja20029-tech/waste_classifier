from django.db import models

WASTE_TYPES = ["plastic", "metal", "organic", "paper", "glass"]
SHAPES = ["bottle", "can", "box", "sheet", "irregular"]
TEXTURES = ["smooth", "rough", "soft", "hard"]
COLORS = ["transparent", "white", "brown", "green", "silver", "black", "blue", "red", "yellow"]

MODEL_CHOICES = [
    ("decision_tree", "Decision Tree"),
    ("random_forest", "Random Forest"),
    ("neural_network", "Neural Network"),
]


def _choices(values):
    return [(v, v.title()) for v in values]


class WasteSample(models.Model):
    """Training data row (stored in MySQL / SQLite)."""
    weight = models.FloatField(help_text="grams")
    size = models.FloatField(help_text="cm (longest side)")
    shape = models.CharField(max_length=20, choices=_choices(SHAPES))
    texture = models.CharField(max_length=20, choices=_choices(TEXTURES))
    color = models.CharField(max_length=20, choices=_choices(COLORS))
    waste_type = models.CharField(max_length=20, choices=_choices(WASTE_TYPES))

    def __str__(self):
        return f"{self.waste_type} ({self.weight} g)"


class PredictionRecord(models.Model):
    """Every prediction made through the website."""
    weight = models.FloatField()
    size = models.FloatField()
    shape = models.CharField(max_length=20)
    texture = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    predicted_type = models.CharField(max_length=20)
    confidence = models.FloatField()
    model_used = models.CharField(max_length=30, choices=MODEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class ModelMetric(models.Model):
    """Accuracy of each algorithm after every training run."""
    model_key = models.CharField(max_length=30, choices=MODEL_CHOICES)
    accuracy = models.FloatField()
    train_size = models.IntegerField()
    test_size = models.IntegerField()
    trained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-trained_at"]
