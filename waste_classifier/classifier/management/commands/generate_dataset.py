import random

from django.core.management.base import BaseCommand

from classifier.models import WasteSample

# (weight range g, size range cm, shapes, textures, colors)
PROFILES = {
    "plastic": ((20, 300), (5, 30), ["bottle", "box", "sheet", "irregular"], ["smooth", "soft"], ["transparent", "blue", "white", "red", "black"]),
    "metal":   ((50, 600), (5, 25), ["can", "box", "irregular"], ["hard", "rough"], ["silver", "black", "red"]),
    "organic": ((50, 800), (3, 25), ["irregular"], ["soft", "rough"], ["brown", "green", "yellow"]),
    "paper":   ((5, 200), (10, 40), ["sheet", "box"], ["rough", "soft"], ["white", "brown", "yellow"]),
    "glass":   ((100, 700), (5, 30), ["bottle", "irregular"], ["smooth", "hard"], ["transparent", "green", "brown"]),
}
SHAPES = ["bottle", "can", "box", "sheet", "irregular"]
TEXTURES = ["smooth", "rough", "soft", "hard"]
COLORS = ["transparent", "white", "brown", "green", "silver", "black", "blue", "red", "yellow"]


class Command(BaseCommand):
    help = "Generate a SYNTHETIC demo dataset. Replace with real data for real use."

    def add_arguments(self, parser):
        parser.add_argument("--per-class", type=int, default=300)

    def handle(self, *args, **opts):
        random.seed(42)
        WasteSample.objects.all().delete()
        rows = []
        for label, (w, s, shapes, textures, colors) in PROFILES.items():
            for _ in range(opts["per_class"]):
                # 8% noise so classes overlap like real life
                noisy = lambda good, pool: random.choice(pool) if random.random() < 0.08 else random.choice(good)
                rows.append(WasteSample(
                    weight=round(random.uniform(*w), 1),
                    size=round(random.uniform(*s), 1),
                    shape=noisy(shapes, SHAPES),
                    texture=noisy(textures, TEXTURES),
                    color=noisy(colors, COLORS),
                    waste_type=label,
                ))
        WasteSample.objects.bulk_create(rows)
        self.stdout.write(self.style.SUCCESS(f"Created {len(rows)} sample rows."))
