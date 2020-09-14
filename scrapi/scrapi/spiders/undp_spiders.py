import scrapy
from tenders.models import Tender
from profiles.models import Profile
from webs.models import Web
from search_settings.models import SearchSettings


class UndpSpiders(scrapy.Spider):
  name = 'undp_spiders'
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

    links_webs = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[4]/a/@href').getall()

    places = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[6]/text()').getall()

    companies = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[2]/text()').getall()

    dates_posteds = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[9]/nobr/text()').getall()

    dates_deadline = response.xpath(
        '//table[@class="standard cellborder"]//tr[@valign="top"]/td[8]/nobr/text()').getall()

    # profiles = Profile.objects.all()
    get_webs = Web.objects.all().filter(
        url='https://procurement-notices.undp.org/')

    for item_get_webs in get_webs:
      get_search_settins = SearchSettings.objects.all().filter(
          country_id=item_get_webs.country_id)

      for item_search_settings in get_search_settins:
        profiles = Profile.objects.all().filter(
            id=item_search_settings.profile_id)

        for item_profile in profiles:
          for item in descriptions:
            words_searchs = item_profile.search_parameters.upper().strip().split(',')
            words_not_searchs = item_profile.discard_parameters.upper().strip().split(',')

            word_key_in = any([words_search in descriptions[descriptions.index(
                item)].upper() for words_search in words_searchs])

            if word_key_in:
              word_key_not_in = any([words_not_search in descriptions[descriptions.index(
                  item)].upper() for words_not_search in words_not_searchs])

              print(words_not_searchs, '*******---', word_key_not_in)
              if word_key_not_in:
                print('*************--- NOT SAVE ---*************')
              else:
                print('*************--- SAVE ---*************')
                print('--*************-')
                print('*' * 10)
                print('\n\n')
                dates_save = f"{dates_posteds[descriptions.index(item)]} - {dates_deadline[descriptions.index(item)]}"
                link = f"https://procurement-notices.undp.org/{links_webs[descriptions.index(item)]}"

                tenders_save = Tender(
                    country_id=item_get_webs.country_id, profile_id=item_profile.id, description=descriptions[descriptions.index(item)], code=titles[descriptions.index(item)], link=link, place_of_execution=places[descriptions.index(item)].rstrip(), awarning_authority=companies[descriptions.index(item)], dates=dates_save)
                tenders_save.save()
