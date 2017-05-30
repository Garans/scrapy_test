import scrapy
import pandas as pd
import re


class PricesAliexpress(scrapy.Spider):
    name = 'headphones'

    prog = re.compile(r'\d+.\d+')

    def start_requests(self):
        url = 'https://www.aliexpress.com/category/63705/earphones-headphones/{}.html?site=glo&tc=af&tag='
        for k in range(15):
            yield scrapy.Request(url.format(k + 1), self.parse)

    def parse(self, response):
        for quote in response.css('#list-items li'):
            right_block = quote.css('.right-block div.right-block-wrap')
            link = right_block.css('.detail h3 a.product::attr(href)').extract_first()
            description = right_block.css('.detail h3 a::text').extract()
            prices = right_block.css('div.infoprice span.price span.value::text').re(r'\d+.\d+')
            price_from = prices[0] if prices else 0
            price_to = prices[1] if len(prices) > 1 else 0
            yield {
                'link': link[2:len(link)], 'description': description, 'price_from': price_from,
                'price_to': price_to
            }
