import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from homepage.models import Product

class Command(BaseCommand):
    help = 'Import products from AliExpress affiliate category links and publish on site'

    affiliate_category_links = [
        'https://s.click.aliexpress.com/e/_oEF2OVm',
        'https://s.click.aliexpress.com/e/_ooNowc8',
        'https://s.click.aliexpress.com/e/_oChpPLm',
        'https://s.click.aliexpress.com/e/_oD66o7a',
        'https://s.click.aliexpress.com/e/_om8VEC8',
        'https://s.click.aliexpress.com/e/_omUah9a',
        'https://s.click.aliexpress.com/e/_ok0LJYu',
        'https://s.click.aliexpress.com/e/_ooFlNku',
    ]

    def handle(self, *args, **options):
        count = 0
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        }

        for link in self.affiliate_category_links:
            self.stdout.write(f'Processing category link: {link}')
            try:
                response = requests.get(link, headers=headers)
                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f'Failed to retrieve page: {response.status_code} for {link}'))
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                # Adjust selectors based on actual AliExpress affiliate page structure
                product_cards = soup.select('.list-item, .product-card, .item, .product-item')

                if not product_cards:
                    self.stdout.write(self.style.WARNING(f'No products found on page: {link}'))
                    continue

                for product in product_cards:
                    try:
                        title_tag = product.select_one('.item-title, .product-title, .title')
                        title = title_tag.get_text(strip=True) if title_tag else 'No title'

                        price_tag = product.select_one('.price-current, .price, .product-price')
                        price = price_tag.get_text(strip=True) if price_tag else 'N/A'

                        image_tag = product.select_one('img')
                        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else ''

                        product_link_tag = product.select_one('a')
                        product_link = product_link_tag['href'] if product_link_tag and 'href' in product_link_tag.attrs else link

                        description_tag = product.select_one('.item-desc, .product-desc, .description')
                        description = description_tag.get_text(strip=True) if description_tag else ''

                        # Save or update product in DB
                        Product.objects.update_or_create(
                            title=title,
                            defaults={
                                'price': price,
                                'description': description,
                                'image_url': image_url,
                                'affiliate_link': product_link,
                                'category': 'Imported Affiliate',
                            }
                        )
                        count += 1
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Failed to process a product: {e}'))
                        continue

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing category link {link}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} products.'))
