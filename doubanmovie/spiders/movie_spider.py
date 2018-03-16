# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from doubanmovie.items import DoubanmovieItem

class MoiveSpider(CrawlSpider):
    name = "doubanmovie"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["http://movie.douban.com/top250"]

    # rules = [
    #     Rule(scrapy.linkextractors.LinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
    #     Rule(scrapy.linkextractors.LinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')), callback="parse_item"),
    # ]

    def parse(self, response):
        for info in response.xpath('//div[@class="item"]'):
            item = DoubanmovieItem()
            item['rank'] = info.xpath('div[@class="pic"]/em/text()').extract_first()
            item['title'] = info.xpath('div[@class="pic"]/a/img/@alt').extract_first()
            item['link'] = info.xpath('div[@class="pic"]/a/@href').extract_first()
            item['star'] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span/text()').extract_first()
            item['rate'] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span/text()').extract_first()
            item['quote'] = info.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract_first()
            yield item

        # 翻页
        next_page = response.xpath('//span[@class="next"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

