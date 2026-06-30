import os

from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import Product
from api.products import products


class Command(BaseCommand):
    help = "Seed the database with the mockup products from api/products.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing products before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            deleted, _ = Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted existing products ({deleted} rows)."))

        created = 0
        for item in products:
            # The mockup '_id' is ignored — Django generates its own primary key.
            # ImageField stores a path RELATIVE to MEDIA_ROOT, so strip the
            # mockup's leading '/images/' and keep only the filename. Django's
            # MEDIA_URL ('/images/') is re-added automatically by .url.
            image_name = os.path.basename(item["image"])
            Product.objects.create(
                user=None,
                name=item["name"],
                image=image_name,
                brand=item["brand"],
                category=item["category"],
                description=item["description"],
                rating=item["rating"],
                numReviews=item["numReviews"],
                price=item["price"],
                countInStock=item["countInStock"],
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} products."))
