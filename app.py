from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# Function to configure headless Chrome
def get_headless_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Function to scrape Amazon for cheapest products
def scrape_amazon(query):
    driver = get_headless_driver()  # Use headless driver
    search_url = f"https://www.amazon.in/s?k={query}"
    driver.get(search_url)
    time.sleep(3)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []
    for item in soup.select('.s-main-slot .s-result-item'):
        name = item.select_one('h2 a span')
        price = item.select_one('.a-price-whole')
        link = item.select_one('h2 a')
        if name and price and link:
            products.append({
                'name': name.text,
                'price': price.text.replace(',', ''),
                'link': "https://www.amazon.in" + link['href'],
                'source': 'Amazon'
            })
    return products[:10]  # Return top 10 products

# Function to scrape eBay for cheapest products
def scrape_ebay(query):
    driver = get_headless_driver()  # Use headless driver
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    driver.get(search_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []
    for item in soup.select('.s-item'):
        name = item.select_one('.s-item__title')
        price = item.select_one('.s-item__price')
        link = item.select_one('.s-item__link')
        if name and price and link:
            products.append({
                'name': name.text,
                'price': price.text.replace('$', '').replace(',', ''),
                'link': link['href'],
                'source': 'eBay'
            })
    return products[:10]  # Return top 10 products

# Function to scrape Flipkart for cheapest products
def scrape_flipkart(query):
    driver = get_headless_driver()  # Use headless driver
    search_url = f"https://www.flipkart.com/search?q={query}"
    driver.get(search_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    products = []
    for item in soup.select('._1AtVbE'):
        name = item.select_one('._4rR01T')
        price = item.select_one('._30jeq3')
        link = item.select_one('a._1fQZEK')
        if name and price and link:
            products.append({
                'name': name.text,
                'price': price.text.replace('₹', '').replace(',', ''),
                'link': "https://www.flipkart.com" + link['href'],
                'source': 'Flipkart'
            })
    return products[:10]  # Return top 10 products

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    query = request.form['query']
    amazon_products = scrape_amazon(query)
    flipkart_products = scrape_flipkart(query)
    ebay_products = scrape_ebay(query)

    all_products = amazon_products + flipkart_products + ebay_products
    # Sort products by price
    all_products = sorted(all_products, key=lambda x: float(x['price'].replace(',', '')))

    return render_template('index.html', products=all_products[:10])  # Return top 10 cheapest products across all sources

if __name__ == '__main__':
    app.run(debug=True)
