# -*- coding: utf-8 -*-

import scrapy
import re
from urllib import unquote

from kodepos.items import KodeposItem


class KodeposNomorNetSpider(scrapy.Spider):

  name = 'kodepos.nomor.net'

  # Instead of start with single url, we split the url based on Province so we can get Province name from the url.
  start_urls = [
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Bali&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 1. Bali
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Bangka%20Belitung&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 2. Bangka Belitung
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Banten&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 3. Banten
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Bengkulu&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 4. Bengkulu
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=DI%20Yogyakarta&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 5. DI Yogyakarta
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=DKI%20Jakarta&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 6. DKI Jakarta
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Gorontalo&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 7. Gorontalo
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Jambi&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 8. Jambi
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Jawa%20Barat&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 9. Jawa Barat
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Jawa%20Tengah&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 10. Jawa Tengah
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Jawa%20Timur&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', #11. Jawa Timur
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Kalimantan%20Barat&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 12. Kalimantan Barat
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Kalimantan%20Selatan&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 13. Kalimantan Selatan
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Kalimantan%20Tengah&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 14. Kalimantan Tengah
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Kalimantan%20Timur&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 15. Kalimantan Timur
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Kalimantan%20Utara&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 16. Kalimantan Utara
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Kepulauan%20Riau&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 17. Kepulauan Riau
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Lampung&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 18. Lampung
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Maluku&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 19. Maluku
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Maluku%20Utara&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 20. Maluku Utara
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Nanggroe%20Aceh%20Darussalam%20(NAD)&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 21. NAD
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Nusa%20Tenggara%20Barat%20(NTB)&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 22. NTB
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Nusa%20Tenggara%20Timur%20(NTT)&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 23. NTT 
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Papua&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 24. Papua
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Papua%20Barat&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 25. Papua Barat
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Riau&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 26. Riau
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Sulawesi%20Barat&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 27. Sulawesi Barat
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Sulawesi%20Selatan&perhal=200&urut=&asc=000101&sby=000000&no1=1&no2=200&kk=2', # 28. Sulawesi Selatan
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Sulawesi%20Tengah&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 29. Sulawesi Tengah
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Sulawesi%20Tenggara&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 30. Sulawesi Tenggara
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Sulawesi%20Utara&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 31. Sulawesi Utara
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Sumatera%20Barat&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 32. Sumatera Barat
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Sumatera%20Selatan&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 33. Sumatera Selatan
    'http://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Sumatera%20Utara&perhal=200&urut=&asc=000101&sby=000000&no1=2&no2=400&kk=0', # 34. Sumatera Utara
  ]

  # page tokens that already crawled (we need this since the urls format is not consistent).
  crawled_pages = []

  def parse(self, response):

    page = self.get_page_number(response.url)
    prov = self.get_province(response.url)
    token = self.get_unique_token(prov, page)

    self.crawled_pages.append(token)

    # START: Parse response
    rows = response.css('tr[bgcolor="#ccffff"]')
    for row in rows:
      cols = row.css('td')

      provinsi = prov
      kodepos = cols[1].css('a.ktu::text').extract_first(default='n/a')
      desa = cols[2].css('a::text').extract_first(default='n/a')
      kode_wil = cols[3].css('a::text').extract_first(default='n/a')
      kecamatan = cols[4].css('a::text').extract_first(default='n/a')
      daerah_t2 = cols[5].css('td::text').extract_first()
      kabupaten_kota = cols[6].css('a::text').extract_first(default='n/a')

      yield KodeposItem(provinsi=provinsi, kodepos=kodepos, desa=desa, kode_wil=kode_wil,
                        kecamatan=kecamatan, daerah_t2=daerah_t2,
                        kabupaten_kota=kabupaten_kota)
    # END: Parse response

    for url in response.css('td a.tpage::attr(href)').extract():

      token = self.get_unique_token_from_url(url)
      already_crawled = (token in self.crawled_pages)

      if not already_crawled:
        yield response.follow(url, self.parse)

  def get_page_number(self, url):
    """
    Returns page number from url.
    """
    url_parts = url.split('=')
    page = url_parts[-1] # page number
    return int(page)

  def get_province(self, url):
    """
    Return province name from url.
    """
    result = re.search(r"jobs=(?P<prov>[\w%\(\)\+ ]*)&", url)
    return unquote(result.group("prov"))

  def get_unique_token(self, prov, page):
    """
    Return unique token from combination of Province and Page number.
    example: kalimantan-barat-25
    """
    cleaned_prov = prov.replace(" ", "-").lower()
    return "%s-%s" % (cleaned_prov, page)

  def get_unique_token_from_url(self, url):
    """
    Return unique token from combination of Province and Page number.
    """
    page = self.get_page_number(url)
    prov = self.get_province(url)
    return self.get_unique_token(prov, page)
