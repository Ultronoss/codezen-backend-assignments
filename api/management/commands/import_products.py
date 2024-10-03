from django.core.management.base import BaseCommand
from api.models import Product
import pandas as pd

class Command(BaseCommand):
    help = 'Import products from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        try:
            df = pd.read_excel(excel_file)
            for _, row in df.iterrows():
                product_name = row['product_name']
                amount = row['amount']
                Product.objects.update_or_create(
                    name=product_name,
                    defaults={'amount': amount}
                )
            self.stdout.write(self.style.SUCCESS('Products imported successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error importing products: {e}'))