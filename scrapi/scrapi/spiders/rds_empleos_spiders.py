import scrapy
from tenders.models import Tender
from profiles.models import Profile
import datetime


# Titulos = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/text()
# Empresa = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[not(contains(@class , "para"))]/text()
# Descripcion //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[@class="para"]/text()
# Lugar = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[0]/text()
# Fecha = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[1]/text()


class RdsEmpleosSpiders(scrapy.Spider):
  name = 'rds_empleados_spiders'
  start_urls = [
      'https://rds-empleos.hn/plazas/category/17'
  ]
  custom_settings = {
      'FEED_URI': 'rds_empleados_spiders.json',
      'FEED_FORMAT': 'json'
  }

  def parse(self, response):

    titles = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/text()').getall()

    links_webs = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/@href').getall()

    companies = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[not(contains(@class , "para"))]/text()').getall()

    descriptions = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[contains(@class, "para")]/text()').getall()

    places = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[1]/text()').getall()

    dates = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[2]/text()').getall()

    profiles = Profile.objects.all()
    for item_profile in profiles:
      for item in titles:
        words_searchs = item_profile.search_parameters.upper().strip().split(',')
        words_not_searchs = item_profile.discard_parameters.upper().strip().split(',')

        word_key_in = any([words_search in titles[titles.index(
            item)].upper() for words_search in words_searchs])

        if word_key_in:
          word_key_not_in = any([words_not_search in titles[titles.index(
              item)].upper() for words_not_search in words_not_searchs])

          if word_key_not_in:
            print('*************--- NOT SAVE ---*************')
          else:
            print('*************--- SAVE ---*************')
            split_date = dates[titles.index(item)].rstrip().split('-')
            dates_save = f"{split_date[0]} - {split_date[1]}"
            link = f"https://rds-empleos.hn/plazas/category/17/{links_webs[titles.index(item)]}"
            code = f"rds_empleados-{titles.index(item)}-{datetime.datetime.now()}"

            tenders_save = Tender(
                country_id=1, profile_id=1, description=titles[titles.index(item)], code=code, link=link, place_of_execution=places[titles.index(item)].rstrip(), awarning_authority=companies[titles.index(item)], dates=dates_save)
            tenders_save.save()
