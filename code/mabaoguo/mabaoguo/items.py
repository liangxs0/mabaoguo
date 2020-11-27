# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MabaoguoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    video_address = scrapy.Field() # 视频url地址
    video_title = scrapy.Field() # 视频标题
    play_number = scrapy.Field() # 视频播放量
    hide_number = scrapy.Field() #弹幕数量
    video_date = scrapy.Field() #视频上传时间
    video_author = scrapy.Field() #视频作者

