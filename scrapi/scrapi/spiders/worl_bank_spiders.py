import scrapy
from tenders.models import Tender


class WorlBankSpiders(scrapy.Spider):
  name = 'worl_bank_spiders'
  start_urls = [
      'https://procurement-notices.undp.org/'
  ]
  custom_settings = {
      'FEED_URI': 'undp_spiders.json',
      'FEED_FORMAT': 'json'
  }

  def parse(self, response):

    titles = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[7]/text()').getall()

    descriptions = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[4]/a/text()').getall()

    places = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[6]/text()').getall()

    companies = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[2]/text()').getall()

    dates_posteds = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[9]/nobr/text()').getall()

    dates_deadline = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[8]/nobr/text()').getall()

    items = []
    for item in titles:

      print('*' * 10)
      print('\n\n')

      dates_save = f"{dates_posteds[titles.index(item)]} - {dates_deadline[titles.index(item)]}"
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
