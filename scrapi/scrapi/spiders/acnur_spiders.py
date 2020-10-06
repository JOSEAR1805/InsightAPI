import scrapy
from scrapy.mail import MailSender
from tenders.models import Tender
from profiles.models import Profile
from django.contrib.auth.models import User
from webs.models import Web
from search_settings.models import SearchSettings

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
        mailer = MailSender(mailfrom="insight@globaldigital-latam.com", smtphost="mail.globaldigital-latam.com",
                            smtpport=587, smtpuser="insight@globaldigital-latam.com", smtppass="Latam5454@")
        emails_users = []

        descriptions = response.xpath(
            '//div[@class="section__wrapper"]/ul[@class="results"]/li/a/h2/text()').getall()

        links_webs = response.xpath(
            '//div[@class="section__wrapper"]/ul[@class="results"]/li/a/@href').getall()

        dates_webs = response.xpath(
            '//div[@class="section__wrapper"]/ul[@class="results"]/li/a/span/text()').getall()

        get_webs = Web.objects.all().filter(
            url='https://www.acnur.org/search')

        for item_get_webs in get_webs:
            get_search_settins = SearchSettings.objects.all().filter(
                country_id=item_get_webs.country_id)

            for item_search_settings in get_search_settins:
                user_send_email = User.objects.get(
                    id=item_search_settings.user_id)
                emails_users.append(user_send_email.email)
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

                            if word_key_not_in:
                                print('*************--- NOT SAVE ---*************')
                            else:
                                link = f"{links_webs[descriptions.index(item)]}"

                                objDate = datetime.strptime(dates_webs[descriptions.index(item)].strip(), "%d %b %Y")
                                tenderUnixDate = time.mktime(objDate.timetuple())

                                if todayUnixDate == tenderUnixDate:
                                    tender_counts = Tender.objects.filter(description=descriptions[descriptions.index(item)], publication_date=dates_webs[descriptions.index(item)].strip()).values()

                                    if len(tender_counts) <= 0:
                                        print('*************--- SAVE ---*************')
                                        tenders_save = Tender(
                                            user_id=item_search_settings.user_id, country_id=item_get_webs.country_id, profile_id=item_profile.id, description=descriptions[descriptions.index(item)], link=link, publication_date=dates_webs[descriptions.index(item)].strip())
                                        tenders_save.save()


        if len(emails_users) > 0:
            mailer.send(to=emails_users,
                        subject="Nuevas licitaciones", body="El sistema ha registrado nuevas licitaciones")
