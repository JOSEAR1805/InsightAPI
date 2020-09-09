import scrapy
from tenders.models import Tender


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

    companies = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[not(contains(@class , "para"))]/text()').getall()

    descriptions = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[contains(@class, "para")]/text()').getall()

    places = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[1]/text()').getall()

    dates = response.xpath(
        '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[2]/text()').getall()

    items = []
    for item in titles:

      print('*' * 10)
      print('\n\n')

      split_date = dates[titles.index(item)].rstrip().split('-')
      dates_save = f"{split_date[0]} - {split_date[1]}"
      tenders_save = Tender(
          country_id=1, profile_id=1, description=descriptions[titles.index(item)], code=titles[titles.index(item)], place_of_execution=places[titles.index(item)].rstrip(), awarning_authority=companies[titles.index(item)], dates=dates_save)
      tenders_save.save()

    print('\n\n')
    print('*' * 10)

    # if titles[titles.index(item)] and companies[titles.index(item)] and descriptions[titles.index(item)]:
    #   items.append({
    #       'title': titles[titles.index(item)],
    #       'company': companies[titles.index(item)],
    #       'descriptions': descriptions[titles.index(item)],
    #   })

    # print(items)
    # yield items
