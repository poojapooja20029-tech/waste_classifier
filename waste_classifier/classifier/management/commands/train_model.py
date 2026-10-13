from django.core.management.base import BaseCommand

from classifier import ml


class Command(BaseCommand):
    help = "Train Decision Tree, Random Forest and Neural Network models."

    def handle(self, *args, **opts):
        for key, acc in ml.train_and_store():
            self.stdout.write(f"{key:15s} accuracy = {acc}%")
        self.stdout.write(self.style.SUCCESS("Training complete."))
