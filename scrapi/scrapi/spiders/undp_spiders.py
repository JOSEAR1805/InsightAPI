import scrapy
from tenders.models import Tender
from profiles.models import Profile
from django.contrib.auth.models import User
from webs.models import Web
from search_settings.models import SearchSettings
import time
from datetime import date, datetime
from django.core.mail import send_mail

today = date.today()
d1 = today.strftime("%d-%b-%y")
objDate = datetime.strptime(d1, '%d-%b-%y')
todayUnixDate = time.mktime(objDate.timetuple())

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
        emails_users = []

        titles = response.xpath('//table[@class="standard cellborder"]//tr[@valign="top"]/td[3]/text()').getall()

        descriptions = response.xpath('//table[@class="standard cellborder"]//tr[@valign="top"]/td[4]/a/text()').getall()

        links_webs = response.xpath('//table[@class="standard cellborder"]//tr[@valign="top"]/td[4]/a/@href').getall()

        places = response.xpath('//table[@class="standard cellborder"]//tr[@valign="top"]/td[6]/text()').getall()

        companies = response.xpath('//table[@class="standard cellborder"]//tr[@valign="top"]/td[2]/text()').getall()

        dates_posteds = response.xpath('//table[@class="standard cellborder"]//tr[@valign="top"]/td[9]/nobr/text()').getall()

        dates_deadline = response.xpath('//table[@class="standard cellborder"]//tr[@valign="top"]/td[8]/nobr/text()').getall()

        get_webs = Web.objects.all().filter(url='https://procurement-notices.undp.org/')

        for item_get_webs in get_webs:
            search_settings = SearchSettings.objects.all().filter(country_id=item_get_webs.country_id)

            for item_search_settings in search_settings:
                users = User.objects.get(id=item_search_settings.user_id)
                profiles = Profile.objects.all().filter(id=item_search_settings.profile_id)

                for item_profile in profiles:
                    for item in descriptions:
                        words_searchs = item_profile.search_parameters.upper().strip().split(',')
                        words_not_searchs = item_profile.discard_parameters.upper().strip().split(',')

                        word_key_in = any([words_search in descriptions[descriptions.index(
                            item)].upper() for words_search in words_searchs])

                        if word_key_in:
                            word_key_not_in = any([words_not_search in descriptions[descriptions.index(
                                item)].upper() for words_not_search in words_not_searchs])

                            if word_key_not_in:
                                print('***** NOT SAVE *****')
                            else:
                                dates_save = f"{dates_posteds[descriptions.index(item)]} - {dates_deadline[descriptions.index(item)]}"
                                link = f"https://procurement-notices.undp.org/{links_webs[descriptions.index(item)]}"

                                objDate = datetime.strptime(dates_posteds[descriptions.index(item)], '%d-%b-%y')
                                tenderUnixDate = time.mktime(objDate.timetuple())

                                if todayUnixDate == tenderUnixDate:
                                    tender_counts = Tender.objects.filter(
                                        description=descriptions[descriptions.index(item)], 
                                        publication_date=dates_posteds[descriptions.index(item)]
                                    ).values()

                                    if len(tender_counts) <= 0:
                                        emails_users.append(users.email)
                                        tenders_save = Tender(
                                            user_id=item_search_settings.user_id, 
                                            country_id=item_get_webs.country_id, 
                                            profile_id=item_profile.id, 
                                            description=descriptions[descriptions.index(item)], 
                                            code=titles[descriptions.index(item)], 
                                            link=link, place_of_execution=places[descriptions.index(item)].rstrip(), 
                                            awarning_authority=companies[descriptions.index(item)], 
                                            publication_date=dates_posteds[descriptions.index(item)], 
                                            closing_date=dates_deadline[descriptions.index(item)],
                                            status="Nuevo"
                                        )

                                        tenders_save.save()
                                        print('***** SAVE *****')

        
        if len(emails_users) > 0:
            emails_users = set(emails_users); #eliminar los correos duplicados
            send_mail(
                'Nueva Licitaciones en Insight Intranet',
                'El sistema ha registrado nuevas licitaciones de la página https://procurement-notices.undp.org/',
                'insight@globaldigital-latam.com',
                emails_users,
            )
            print('***** SEND EMAIL *****')