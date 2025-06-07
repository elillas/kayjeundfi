import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.core.management.base import BaseCommand
from homepage.models import Product
from webdriver_manager.chrome import ChromeDriverManager

def resolve_affiliate_link(short_url):
    try:
        response = requests.get(short_url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print(f"Erreur pendant la résolution du lien : {e}")
        return None

class Command(BaseCommand):
    help = 'Import products from AliExpress affiliate category links using Selenium'

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
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36")
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 15)

        count = 0

        for link in self.affiliate_category_links:
            self.stdout.write(f'Processing category link: {link}')
            real_link = resolve_affiliate_link(link)
            if not real_link:
                self.stdout.write(self.style.WARNING(f'Could not resolve real link for: {link}'))
                continue
            try:
                driver.get(real_link)

                # Wait for product container to be present
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.JIIxO')))
                except TimeoutException:
                    self.stdout.write(self.style.WARNING(f'Timeout waiting for products on page: {real_link}'))
                    continue

                # Scroll down to load more products if needed
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                # Try clicking "Load More" button if present
                try:
                    load_more_button = driver.find_element(By.CSS_SELECTOR, 'button._3fZQq')
                    while load_more_button.is_displayed():
                        try:
                            load_more_button.click()
                            time.sleep(3)
                        except ElementClickInterceptedException:
                            break
                        load_more_button = driver.find_element(By.CSS_SELECTOR, 'button._3fZQq')
                except NoSuchElementException:
                    pass

                product_cards = driver.find_elements(By.CSS_SELECTOR, 'div.JIIxO')

                if not product_cards:
                    self.stdout.write(self.style.WARNING(f'No products found on page: {real_link}'))
                    continue

                for product in product_cards:
                    try:
                        title = ''
                        price = ''
                        description = ''
                        image_url = ''
                        product_link = ''

                        try:
                            title = product.find_element(By.CSS_SELECTOR, 'a._3t7zg').text
                        except NoSuchElementException:
                            title = 'No title'

                        try:
                            price = product.find_element(By.CSS_SELECTOR, 'div.mGXnE._37W_B').text
                        except NoSuchElementException:
                            price = 'N/A'

                        try:
                            description = ''
                        except NoSuchElementException:
                            description = ''

                        try:
                            image_elem = product.find_element(By.TAG_NAME, 'img')
                            image_url = image_elem.get_attribute('src')
                        except NoSuchElementException:
                            image_url = ''

                        try:
                            link_elem = product.find_element(By.CSS_SELECTOR, 'a._3t7zg')
                            product_link = link_elem.get_attribute('href')
                        except NoSuchElementException:
                            product_link = real_link

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
                self.stdout.write(self.style.ERROR(f'Error processing category link {real_link}: {e}'))

        driver.quit()
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} products.'))
