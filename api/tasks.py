from celery import shared_task
import pandas as pd
from .models import Product

@shared_task
def import_products(file_path):
    # Read Excel file
    data = pd.read_excel(file_path)
    
    # Iterate through rows and create Product objects
    for _, row in data.iterrows():
        Product.objects.update_or_create(
            name=row['product_name'],
            defaults={'amount': row['amount']},
        )
    return f"Imported {len(data)} products successfully."
