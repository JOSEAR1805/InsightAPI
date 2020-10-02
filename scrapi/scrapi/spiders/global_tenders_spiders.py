import scrapy
from tenders.models import Tender
from scrapy.mail import MailSender
from profiles.models import Profile
from webs.models import Web
from django.contrib.auth.models import User
from search_settings.models import SearchSettings
import datetime


class GlobalTendersSpiders(scrapy.Spider):
    name = 'global_tenders_spiders'
    start_urls = [
        'https://www.globaltenders.com/government-tenders-latin-america.php'
    ]
    custom_settings = {
        'FEED_URI': 'global_tenders_spiders.json',
        'FEED_FORMAT': 'json'
    }

    def parse(self, response):

        mailer = MailSender(mailfrom="notificaciones@insightmarketingca.com", smtphost="smtp.insightmarketingca.com",
                            smtpport=587, smtpuser="notificaciones@insightmarketingca.com", smtppass="Latam5454@")
        emails_users = []

        descriptions = response.xpath(
            '//div[@class="classWithPad"]/div[4]/div/table//tr/td[1]/table/tr[3]/td/table/tr/td[2]/text()').getall()

        titles = response.xpath(
            '//div[@class="classWithPad"]/div[4]/div/table//tr/td[1]/table/tr[1]/td/table/tr/td[2]/text()').getall()

        links_webs = response.xpath(
            '//div[@class="classWithPad"]/div[4]/div/table//tr/td[1]/table/tr[5]/td/table/tr/td[2]/a/@href').getall()

        places = response.xpath(
            '//div[@class="classWithPad"]/div[4]/div/table//tr/td[1]/table/tr/td/table/tr/td[4]/text()').getall()

        dates_webs = response.xpath(
            '//div[@class="classWithPad"]/div[4]/div/table//tr/td[1]/table/tr[4]/td/table/tr/td[2]/text()').getall()

        get_webs = Web.objects.all().filter(
            url='https://www.globaltenders.com/government-tenders-latin-america.php')

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
                                print('*************--- SAVE ---*************')
                                dates_save = f"{dates_webs[descriptions.index(item)].rstrip()}"
                                link = f"{links_webs[descriptions.index(item)]}"

                                tenders_save = Tender(
                                    user_id=item_search_settings.user_id, country_id=item_get_webs.country_id, profile_id=item_profile.id, description=descriptions[descriptions.index(item)], link=link, place_of_execution=places[descriptions.index(item)].rstrip(), closing_date=dates_save)
                                tenders_save.save()

        if len(emails_users) > 0:
            mailer.send(to=emails_users,
                        subject="Nuevas licitaciones", body="El sistema ha registrado nuevas licitaciones")
