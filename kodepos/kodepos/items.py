# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KodeposItem(scrapy.Item):
  token = scrapy.Field()
  provinsi = scrapy.Field()
  daerah_t2 = scrapy.Field() # Daerah Tingkat 2
  kabupaten_kota = scrapy.Field()
  kecamatan = scrapy.Field()
  desa = scrapy.Field()
  kodepos = scrapy.Field()
