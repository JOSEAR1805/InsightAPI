import scrapy

# Titulos = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/text()
# Empresa = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[not(contains(@class , "para"))]/text()
# Descripcion //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[@class="para"]/text()


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

    items = []
    for item in titles:

      print('*' * 10)
      print('\n\n')

      print({
          'title': titles[titles.index(item)],
          'company': companies[titles.index(item)],
          'descriptions': descriptions[titles.index(item)],
      })

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
