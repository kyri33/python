from scrapy.loader import ItemLoader
from first_scrapy.items import QuoteItem 
import scrapy

class  QuotesSpider(scrapy.Spider):
    
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        self.logger.info('hello this is my first spider')
        quotes = response.css('div.quote')
        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector = quote)
            loader.add_css('quote_content', '.text::text')
            loader.add_css('tags', '.tag::text')
            loader.add_css('makaka', 'div.makaka::text')
            quote_item = loader.load_item()
            '''
            yield {
                'text': quote.css('.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('.tag::text').getall()
            }
            '''
            author_link = quote.css('small.author + a')[0]
            self.logger.info('get author page url')
            yield response.follow(author_link, callback=self.parse_author, meta={'quote_item': quote_item})
        
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, selector = response)
        loader.add_css('author_name', 'h3.author-title::text')
        loader.add_css('author_birthdate', 'span.author-born-date::text')
        loader.add_css('author_bornlocation', 'span.author-born-location::text')
        loader.add_css('author_bio', 'div.author-description::text')
        yield loader.load_item()
        '''
        yield {
            'author_name': response.css('h3.author-title::text').get(),
            'author_birth': response.css('span.author-born-date::text').get(),
            'author_location': response.css('span.author-born-location::text').get(),
            'author_bio': response.css('div.author-description::text').get()
        }
        '''
