# -*- coding: utf-8 -*-
import scrapy
# 导入链接提取器
from scrapy.linkextractors import LinkExtractor
# 导入CrawlSpider和Rule规则类
from scrapy.spiders import Rule
from dushuproject.items import DushuprojectItem

from scrapy_redis.spiders import RedisCrawlSpider

## 分布式爬取


class DuCrawl(RedisCrawlSpider):
    name = 'ducrawl_redis'

    # 这个列表替换了那个构造方法
    allowed_domains = ['www.dushu.com']
    redis_key = 'ducrawl:start_urls'

    # 规则1：提取所有的页码链接
    page_link = LinkExtractor(allow=r'/book/1175_\d+\.html$')
    # 规则2：提取所有的book详情链接
    detail_link = LinkExtractor(allow=r'/book/\d+/')

    rules = (
        Rule(page_link, follow=True),
        Rule(detail_link, callback='parse_info')
    )

    def parse_info(self, response):
        # 创建一个item
        item = DushuprojectItem()
        # 获取其它信息
        item['book_image_url'] = response.xpath('//div[@class="book-pic"]/div[@class="pic"]/img/@src').extract_first()
        item['book_name'] = response.xpath('//div[@class="book-pic"]/div[@class="pic"]/img/@alt').extract_first()
        item['book_author'] = self.parse_author(response)
        # 获取书本价格
        item['book_price'] = response.xpath('//div[@class="book-details"]//span/text()').extract_first()
        # 获取书本简介
        item['book_info'] = response.xpath('//div[@class="book-summary"]/div/div/text()').extract_first()
        # 获取出版社信息
        item['book_publish'] = response.xpath('//div[@class="book-details"]//table//tr[2]/td[2]/a/text()').extract_first()
        yield item

    # 获取作者的函数
    def parse_author(self, response):
        # 先获取这个列表
        author = response.xpath('//div[@id="ctl00_c1_bookleft"]/table//tr[1]//td[2]').xpath('string(.)').extract_first()
        return author
