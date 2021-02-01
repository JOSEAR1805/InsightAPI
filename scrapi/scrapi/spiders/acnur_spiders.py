import scrapy
from tenders.models import Tender
from profiles.models import Profile
from django.contrib.auth.models import User
from webs.models import Web
from auth_user.models import Privilege
from search_settings.models import SearchSettings
from django.core.mail import send_mail
import time
from datetime import date, datetime

today = date.today()
d1 = today.strftime("%d %b %Y")
objDate = datetime.strptime(d1, '%d %b %Y')
todayUnixDate = time.mktime(objDate.timetuple())

class AcnurSpiders(scrapy.Spider):
    name = 'acnur_spiders'
    start_urls = [
        'https://www.acnur.org/search'
    ]
    custom_settings = {
        'FEED_URI': 'acnur_spiders.json',
        'FEED_FORMAT': 'json'
    }

    def parse(self, response):
        emails_users = []

        descriptions = response.xpath('//div[@class="section__wrapper"]/ul[@class="results"]/li/a/h2/text()').getall()

        links_webs = response.xpath('//div[@class="section__wrapper"]/ul[@class="results"]/li/a/@href').getall()

        dates_webs = response.xpath('//div[@class="section__wrapper"]/ul[@class="results"]/li/a/span[@class="date--type"]/text()').getall()

        get_webs = Web.objects.all().filter(url='https://www.acnur.org/search')

        for item_get_webs in get_webs:
            
            for item in descriptions:
                words_searchs = item_get_webs.search_parameters.upper().strip().split(',')

                word_key_in = any([words_search in descriptions[descriptions.index(item)].upper() for words_search in words_searchs])

                if word_key_in:
                            
                    link = f"{links_webs[descriptions.index(item)]}"

                    objDate = datetime.strptime(dates_webs[descriptions.index(item)].strip(), "%d %b %Y")
                    tenderUnixDate = time.mktime(objDate.timetuple())

                    if todayUnixDate == tenderUnixDate:
                        tender_counts = Tender.objects.filter(
                            description=descriptions[descriptions.index(item)], 
                            publication_date=dates_webs[descriptions.index(item)].strip()
                        ).values()

                        if len(tender_counts) <= 0:
                            tenders_save = Tender(
                                country_id=item_get_webs.country_id, 
                                description=descriptions[descriptions.index(item)], 
                                link=link, 
                                publication_date=dates_webs[descriptions.index(item)].strip(),
                                status="Nuevo"
                            )

                            tenders_save.save()
                            print('***** SAVE *****')

                            # buscar las direcciones de correo a enviar el email
                            userPrivileges = Privilege.objects.all()
                            for userPrivilege in userPrivileges:
                                countries_ids = userPrivilege.countries_ids.upper().strip().split(',')
                                if len(countries_ids) > 0:
                                    for country_id in countries_ids:
                                        if str(item_get_webs.country_id) == country_id.strip():
                                            users = User.objects.all().filter(id=userPrivilege.user_id)
                                            for user in users:
                                                emails_users.append(user.email)


        if len(emails_users) > 0:
            emails_users = set(emails_users); #eliminar los correos duplicados
            print(emails_users)

            send_mail(
                'Nueva Licitaciones en Insight Intranet',
                'El sistema ha registrado nuevas licitaciones de la página https://www.acnur.org/search',
                'insight@globaldigital-latam.com',
                emails_users,
            )
            print('***** SEND EMAIL *****')
