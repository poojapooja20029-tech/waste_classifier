from threading import Lock
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, render

from . import ml
from .forms import PredictForm
from .models import MODEL_CHOICES, ModelMetric, PredictionRecord, WasteSample
training_lock = Lock()


def home(request):
    return render(request, "classifier/index.html", {
        "samples": WasteSample.objects.count(),
        "predictions": PredictionRecord.objects.count(),
    })


def predict_view(request):
    result = None
    form = PredictForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        try:
            waste_type, conf = ml.predict(d["model_used"], {k: d[k] for k in ml.FEATURES})
        except FileNotFoundError as e:
            messages.error(request, str(e))
        else:
            PredictionRecord.objects.create(
                weight=d["weight"], size=d["size"], shape=d["shape"],
                texture=d["texture"], color=d["color"],
                predicted_type=waste_type, confidence=conf, model_used=d["model_used"],
            )
            result = {"type": waste_type, "confidence": conf}
    return render(request, "classifier/predict.html", {"form": form, "result": result})


def history(request):
    return render(request, "classifier/history.html", {
        "records": PredictionRecord.objects.all()[:100]
    })


def dashboard(request):
    metrics = []
    for key, label in MODEL_CHOICES:
        m = ModelMetric.objects.filter(model_key=key).first()  # latest run
        metrics.append({"label": label, "m": m})
    distribution = (WasteSample.objects.values("waste_type")
                    .annotate(count=Count("id")).order_by("-count"))
    return render(request, "classifier/dashboard.html", {
        "metrics": metrics, "distribution": distribution,
        "total": WasteSample.objects.count(),
    })




def train_view(request):
    if request.method != "POST":
        return redirect("dashboard")

    if not training_lock.acquire(blocking=False):
        messages.warning(
            request,
            "Training is already in progress. Please wait."
        )
        return redirect("dashboard")

    try:
        results = ml.train_and_store()
        messages.success(
            request,
            "All 3 models trained successfully."
        )
    except Exception as e:
        messages.error(request, f"Training failed: {e}")
    finally:
        training_lock.release()

    return redirect("dashboard")