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
d1 = today.strftime("%d %b %Y")
objDate = datetime.strptime(d1, '%d %b %Y')
todayUnixDate = time.mktime(objDate.timetuple())

class IomSpiders(scrapy.Spider):
    name = 'iom_spiders'
    start_urls = [
        'https://www.iom.int/procurement-opportunities'
    ]
    custom_settings = {
        'FEED_URI': 'iom_spiders.json',
        'FEED_FORMAT': 'json'
    }

    def parse(self, response):
        emails_users = []

        titles = response.xpath('//div[@class="view-content"]/table[1]/tbody/tr/td[1]/text()').getall()

        descriptions = response.xpath('//div[@class="view-content"]/table[1]/tbody/tr/td[2]/a/text()').getall()

        links_webs = response.xpath('//div[@class="view-content"]/table[1]/tbody/tr/td[2]/a/@href').getall()

        places = response.xpath('//div[@class="view-content"]/table[1]/tbody/tr/td[9]/text()').getall()

        dates_posteds = response.xpath('//div[@class="view-content"]/table[1]/tbody/tr/td[7]/span/text()').getall()

        dates_deadline = response.xpath('//div[@class="view-content"]/table[1]/tbody/tr/td[8]/span/text()').getall()

        get_webs = Web.objects.all().filter(url='https://www.iom.int/procurement-opportunities')

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
                                link = f"{links_webs[descriptions.index(item)]}"

                                objDate = datetime.strptime(dates_posteds[descriptions.index(item)].strip(), '%d %b %Y')
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
                                            link=link, 
                                            publication_date=dates_posteds[descriptions.index(item)], 
                                            closing_date=dates_deadline[descriptions.index(item)]
                                        )
                                        tenders_save.save()
                                        print('***** SAVE *****')


        if len(emails_users) > 0:
            emails_users = set(emails_users); #eliminar los correos duplicados
            send_mail(
                'Nueva Licitaciones en Insight Intranet',
                'El sistema ha registrado nuevas licitaciones de la página https://www.iom.int/procurement-opportunities',
                'insight@globaldigital-latam.com',
                emails_users,
            )
            print('***** SEND EMAIL *****')
