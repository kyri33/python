# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time

class CapeunionmartSpider(scrapy.Spider):
    name = 'capeunionmart'
    allowed_domains = ['capeunionmart.co.za']
    start_urls = ['https://capeunionmart.co.za/']

    def parse(self, response):
        self.driver = webdriver.Chrome()
        for link in response.css('li.parentclass-Deals').css('td')[0].css('a::attr(href)').getall():
            self.driver.get(link)
            self.selenium_parse()


    def selenium_parse(self):
        response = Selector(text = self.driver.page_source)

        # TODO OPEN EACH SPECIAL FOR MORE INFO AND BETTER IMAGES
        for special in response.css('li.item'):
            voucherTitle = special.css('h5.product-name').css('a::text').get()
            oldPrice = special.css('p.old-price').css('span::text').get()
            newPrice = special.css('p.special-price').css('span::text').get()
            voucherImage = special.css('img::attr(src)').get()
            specialSource = special.css('a::attr(href)').get()
            u_id = specialSource
            print({
                'voucherTitle': voucherTitle,
                'oldPrice': oldPrice,
                'newPrice': newPrice,
                'voucherImage': voucherImage,
                'specialSource': specialSource,
                'u_id': u_id
            })
        
        if response.css('li.next').get() != None:
            element = self.driver.find_element_by_xpath('//a[@title="Next"]')
            self.driver.execute_script('arguments[0].click();', element)
            time.sleep(2)
            self.selenium_parse()
