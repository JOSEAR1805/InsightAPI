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
d1 = today.strftime('%d/%m/%Y')
objDate = datetime.strptime(d1, '%d/%m/%Y')
todayUnixDate = time.mktime(objDate.timetuple())

class BciesSpiders(scrapy.Spider):
    name = 'bcies_spiders'
    start_urls = [
        'https://adquisiciones.bcie.org/avisos-de-adquisicion'
    ]
    custom_settings = {
        'FEED_URI': 'bcies_spiders.json',
        'FEED_FORMAT': 'json'
    }

    def parse(self, response):
        emails_users = []

        codes = response.xpath('//table[@id="customtables"]//tbody/tr/td[1]/text()').getall()

        titles = response.xpath('//table[@id="customtables"]//tbody/tr/td[2]/a/text()').getall()

        links_webs = response.xpath('//table[@id="customtables"]//tbody/tr/td[2]/a/@href').getall()

        places = response.xpath('//table[@id="customtables"]//tbody/tr/td[3]/text()').getall()

        dates1 = response.xpath('//table[@id="customtables"]//tbody/tr/td[4]/text()').getall()

        dates2 = response.xpath('//table[@id="customtables"]//tbody/tr/td[5]/text()').getall()

        get_webs = Web.objects.all().filter(url='https://adquisiciones.bcie.org/avisos-de-adquisicion')

        for item_get_webs in get_webs:
            search_settings = SearchSettings.objects.all().filter(country_id=item_get_webs.country_id)

            for item_search_settings in search_settings:
                users = User.objects.get(id=item_search_settings.user_id)
                profiles = Profile.objects.all().filter(id=item_search_settings.profile_id)

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
                                print('***** NOT SAVE *****')
                            else:
                                link = f'{links_webs[titles.index(item)]}'

                                objDate = datetime.strptime(dates1[titles.index(item)].strip(), '%d/%m/%Y')
                                tenderUnixDate = time.mktime(objDate.timetuple())

                                if todayUnixDate == tenderUnixDate:
                                    tender_counts = Tender.objects.filter(
                                        description=titles[titles.index(item)], 
                                        publication_date=dates1[titles.index(item)].strip()
                                    ).values()

                                    if len(tender_counts) <= 0:
                                        emails_users.append(users.email)
                                        tenders_save = Tender(
                                            user_id=item_search_settings.user_id, 
                                            country_id=item_get_webs.country_id, 
                                            profile_id=item_profile.id, 
                                            description=titles[titles.index(item)], 
                                            code=codes[titles.index(item)], 
                                            link=link, 
                                            place_of_execution=places[titles.index(item)].rstrip(), 
                                            publication_date=dates1[titles.index(item)].strip(), 
                                            closing_date=dates2[titles.index(item)].strip()
                                        )
                                        tenders_save.save()
                                        print('***** SAVE *****')


        if len(emails_users) > 0:
            emails_users = set(emails_users); #eliminar los correos duplicados
            send_mail(
                'Nueva Licitaciones en Insight Intranet',
                'El sistema ha registrado nuevas licitaciones de la página https://adquisiciones.bcie.org/avisos-de-adquisicion',
                'insight@globaldigital-latam.com',
                emails_users,
            )
            print('***** SEND EMAIL *****')
