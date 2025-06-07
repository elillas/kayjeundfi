from django.core.management.base import BaseCommand
from homepage.models import HomepageSoftware
import requests

class Command(BaseCommand):
    help = 'Import products from affiliate API and add/update HomepageSoftware entries'

    def handle(self, *args, **options):
        self.stdout.write('Starting import of affiliate products...')
        # Placeholder for API URL and headers - to be updated when API details are available
        api_url = 'https://api.example.com/products'
        headers = {
            'Authorization': 'Bearer YOUR_API_KEY',
            'Accept': 'application/json',
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            products = response.json().get('products', [])
            for product in products:
                title = product.get('title')
                image_url = product.get('image_url')
                price = product.get('price')
                description = product.get('description', '')
                affiliate_link = product.get('affiliate_link')

                # Create or update product in database
                obj, created = HomepageSoftware.objects.update_or_create(
                    title=title,
                    defaults={
                        'price': price,
                        'description': description,
                        'affiliate_link': affiliate_link,
                        # Image handling would require downloading and saving the image file
                    }
                )
                if created:
                    self.stdout.write(f'Added new product: {title}')
                else:
                    self.stdout.write(f'Updated product: {title}')
            self.stdout.write('Import completed successfully.')
        except requests.RequestException as e:
            self.stderr.write(f'Error fetching products from API: {e}')
