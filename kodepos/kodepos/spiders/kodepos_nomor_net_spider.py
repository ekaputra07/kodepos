import scrapy

class KodeposNomorNetSpider(scrapy.Spider):

  name = 'kodepos.nomor.net'

  start_urls = [
    # 'http://kodepos.nomor.net/_kodepos.php?_i=kecamatan-kodepos&daerah=&jobs=&perhal=200&urut=&asc=001001&sby=000000&no1=2&no2=7200&kk=0'
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=&jobs=&perhal=1000&urut=&asc=000101&sby=000000&no1=2&no2=9600&kk=0'
  ]

  # page number that already crawled.
  crawled_pages = []

  def parse(self, response):

    page = self.get_page_number(response.url)
    self.crawled_pages.append(page)

    yield {
      'page': page,
      'url': response.url
    }

    for url in response.css('td a.tpage::attr(href)').extract():

      already_crawled = (self.get_page_number(url) in self.crawled_pages)

      if not already_crawled:
        yield response.follow(url, self.parse)

  def get_page_number(self, url):
    """
    Returns page number from specified url.
    """
    url_parts = url.split('=')
    page = url_parts[-1] # page number
    return int(page)
      