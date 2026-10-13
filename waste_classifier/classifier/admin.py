from django.contrib import admin
from .models import ModelMetric, PredictionRecord, WasteSample

admin.site.register(WasteSample)
admin.site.register(PredictionRecord)
admin.site.register(ModelMetric)
