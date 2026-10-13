import csv

from django.core.management.base import BaseCommand

from classifier.models import WasteSample


class Command(BaseCommand):
    help = "Import real data. CSV header: weight,size,shape,texture,color,waste_type"

    def add_arguments(self, parser):
        parser.add_argument("csv_path")

    def handle(self, *args, **opts):
        count = 0
        with open(opts["csv_path"], newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                WasteSample.objects.create(
                    weight=float(r["weight"]), size=float(r["size"]),
                    shape=r["shape"].strip().lower(), texture=r["texture"].strip().lower(),
                    color=r["color"].strip().lower(), waste_type=r["waste_type"].strip().lower(),
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f"Imported {count} rows."))
