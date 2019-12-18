import scrapy

class firstSpider(scrapy.Spider):
    name = 'first'
    allowed_domains=['ajpg.net']
    
    start_urls = [
        'https://www.ajpg.net/about.php',
        'https://www.ajpg.net/retail.php'
    ]
    def parse(self, response):
        filename = response.url.split('/')[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
