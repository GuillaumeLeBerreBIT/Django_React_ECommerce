import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Product
from api.products import products

for p in products:
        
    if Product.objects.filter(_id=p.get('_id')).exists():
        continue
    
    Product.objects.create(
        name=p['name'],
        brand=p['brand'],
        category=p['category'],
        description=p['description'],
        rating=p['rating'],
        numReviews=p['numReviews'],
        price=p['price'],
        countInStock=p['countInStock'],
    )
print(f"Seeded {Product.objects.count()} products successfully.")
