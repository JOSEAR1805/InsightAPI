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
d1 = today.strftime("%b %dº, %Y")
objDate = datetime.strptime(d1, '%b %dº, %Y')
todayUnixDate = time.mktime(objDate.timetuple())

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
        emails_users = []

        titles = response.xpath('//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/text()').getall()

        links_webs = response.xpath('//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/@href').getall()

        companies = response.xpath('//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[not(contains(@class , "para"))]/text()').getall()

        descriptions = response.xpath('//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[contains(@class, "para")]/text()').getall()

        places = response.xpath('//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[1]/text()').getall()

        dates = response.xpath('//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[2]/text()').getall()

        get_webs = Web.objects.all().filter(url='https://rds-empleos.hn/plazas/category/17')

        for item_get_webs in get_webs:
            search_settings = SearchSettings.objects.all().filter(country_id=item_get_webs.country_id)

            for item_search_settings in search_settings:
                users = User.objects.get(id=item_search_settings.user_id)
                profiles = Profile.objects.all().filter(id=item_search_settings.profile_id)

                for item_profile in profiles:
                    for item in titles:
                        # words_searchs = item_profile.search_parameters.upper().strip().split(',')
                        # words_not_searchs = item_profile.discard_parameters.upper().strip().split(',')

                        # word_key_in = any([words_search in titles[titles.index(item)].upper() for words_search in words_searchs])

                        # if word_key_in:
                        #     word_key_not_in = any([words_not_search in titles[titles.index(
                        #         item)].upper() for words_not_search in words_not_searchs])

                        #     if word_key_not_in:
                        #         print('***** NOT SAVE *****')
                        #     else:
                        link = f"https://rds-empleos.hn/plazas/category/17/{links_webs[titles.index(item)]}"

                        split_date = dates[titles.index(item)].split('-')

                        objDate = datetime.strptime(split_date[0].strip(), '%b %dº, %Y')
                        tenderUnixDate = time.mktime(objDate.timetuple())

                        if todayUnixDate == tenderUnixDate:
                            tender_counts = Tender.objects.filter(
                                description=titles[titles.index(item)], 
                                publication_date=split_date[0].strip()
                            ).values()

                            if len(tender_counts) <= 0:
                                emails_users.append(users.email)
                                tenders_save = Tender(
                                    user_id=item_search_settings.user_id, 
                                    country_id=item_get_webs.country_id, 
                                    profile_id=item_profile.id, 
                                    description=titles[titles.index(item)], 
                                    link=link, 
                                    place_of_execution=places[titles.index(item)].rstrip(), 
                                    awarning_authority=companies[titles.index(item)], 
                                    publication_date=split_date[0].strip(), 
                                    closing_date=split_date[1].strip(),
                                    status="Nuevo"
                                )
                                tenders_save.save()
                                print('***** SAVE *****')

        if len(emails_users) > 0:
            emails_users = set(emails_users); #eliminar los correos duplicados
            send_mail(
                'Nueva Licitaciones en Insight Intranet',
                'El sistema ha registrado nuevas licitaciones de la página https://rds-empleos.hn/plazas/category/17',
                'insight@globaldigital-latam.com',
                emails_users,
            )
            print('***** SEND EMAIL *****')
