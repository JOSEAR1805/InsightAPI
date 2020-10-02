import scrapy
from tenders.models import Tender
from scrapy.mail import MailSender
from profiles.models import Profile
from django.contrib.auth.models import User
from webs.models import Web
from search_settings.models import SearchSettings


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

        mailer = MailSender(mailfrom="notificaciones@insightmarketingca.com", smtphost="smtp.insightmarketingca.com",
                            smtpport=587, smtpuser="notificaciones@insightmarketingca.com", smtppass="Latam5454@")
        emails_users = []

        titles = response.xpath(
            '//div[@class="view-content"]/table[1]/tbody/tr/td[1]/text()').getall()

        descriptions = response.xpath(
            '//div[@class="view-content"]/table[1]/tbody/tr/td[2]/a/text()').getall()

        links_webs = response.xpath(
            '//div[@class="view-content"]/table[1]/tbody/tr/td[2]/a/@href').getall()

        places = response.xpath(
            '//div[@class="view-content"]/table[1]/tbody/tr/td[9]/text()').getall()

        dates_posteds = response.xpath(
            '//div[@class="view-content"]/table[1]/tbody/tr/td[7]/span/text()').getall()

        dates_deadline = response.xpath(
            '//div[@class="view-content"]/table[1]/tbody/tr/td[8]/span/text()').getall()

        get_webs = Web.objects.all().filter(
            url='https://www.iom.int/procurement-opportunities')

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

                            print(words_not_searchs,
                                  '*******---', word_key_not_in)
                            if word_key_not_in:
                                print('*************--- NOT SAVE ---*************')
                            else:
                                print('*' * 10)
                                print('\n\n')
                                dates_save = f"{dates_posteds[descriptions.index(item)]} - {dates_deadline[descriptions.index(item)]}"
                                link = f"{links_webs[descriptions.index(item)]}"

                                tenders_save = Tender(
                                    user_id=item_search_settings.user_id, country_id=item_get_webs.country_id, profile_id=item_profile.id, description=descriptions[descriptions.index(item)], code=titles[descriptions.index(item)], link=link, publication_date=dates_posteds[descriptions.index(item)], closing_date=dates_deadline[descriptions.index(item)])
                                tenders_save.save()

        if len(emails_users) > 0:
            mailer.send(to=emails_users,
                        subject="Nuevas licitaciones", body="El sistema ha registrado nuevas licitaciones")
