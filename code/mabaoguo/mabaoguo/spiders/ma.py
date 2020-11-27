import scrapy
from scrapy.log import logger
from urllib.parse import urljoin
from scrapy import Selector
from ..items import MabaoguoItem
import time
import random

class MaSpider(scrapy.Spider):
    name = 'ma'
    # allowed_domains = ['search.bilibili.com']
    start_urls = ['http://search.bilibili.com/']
    base_url = 'https://search.bilibili.com/all?keyword=%E9%A9%AC%E4%BF%9D%E5%9B%BD&from_source=nav_search&spm_id_from=333.851.b_696e7465726e6174696f6e616c486561646572.9&page={page}'
    def start_requests(self):
        for page in range(2,51):
            url = self.base_url.format(page=page)
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        if response.status != 200:
            return None
        #网页获取成功,//*[@id="all-list"]/div[1]/div[2]/ul/li[1]/a
        info_s = response.css('.video-item.matrix').extract()
        for info in info_s:
            item = MabaoguoItem()
            info = Selector(text=info)
            item['video_address'] = urljoin('https://', info.css('a[class="img-anchor"]::attr(href)').extract_first().replace("//",""))
            item['video_title'] = info.css('.info a::attr("title")').extract_first()
            item['play_number'] = info.css('.so-icon.watch-num::text').extract_first().replace(" ","").replace("\n","")
            item['hide_number'] = info.css('.so-icon.hide::text').extract_first().replace(" ","").replace("\n","")
            item['video_date'] = info.css('.so-icon.time::text').extract_first().replace(" ","").replace("\n","")
            item['video_author'] = info.css('.so-icon a[class="up-name"]::text').extract_first().replace(" ","").replace("\n","")
            yield item





