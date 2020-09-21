import scrapy
from tenders.models import Tender
from scrapy.mail import MailSender
from profiles.models import Profile
from django.contrib.auth.models import User
from webs.models import Web
from search_settings.models import SearchSettings
import datetime


# Titulos = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/text()
# Empresa = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[not(contains(@class , "para"))]/text()
# Descripcion //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[@class="para"]/text()
# Lugar = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[0]/text()
# Fecha = //ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[1]/text()


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

        mailer = MailSender(mailfrom="joseartigasdev@gmail.com", smtphost="smtp.gmail.com",
                            smtpport=587, smtpuser="joseartigasdev@gmail.com", smtppass="developer123*")
        emails_users = []

        titles = response.xpath(
            '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/text()').getall()

        links_webs = response.xpath(
            '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//h3/a/@href').getall()

        companies = response.xpath(
            '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[not(contains(@class , "para"))]/text()').getall()

        descriptions = response.xpath(
            '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//p[contains(@class, "para")]/text()').getall()

        places = response.xpath(
            '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[1]/text()').getall()

        dates = response.xpath(
            '//ul[contains(@class, "listService")]//div[@class="listWrpService featured-wrap"]//ul[@class="featureInfo innerfeat"]/li[2]/text()').getall()

        get_webs = Web.objects.all().filter(
            url='https://rds-empleos.hn/plazas/category/17')

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
                    for item in titles:
                        words_searchs = item_profile.search_parameters.upper().strip().split(',')
                        words_not_searchs = item_profile.discard_parameters.upper().strip().split(',')

                        word_key_in = any([words_search in titles[titles.index(
                            item)].upper() for words_search in words_searchs])

                        if word_key_in:
                            word_key_not_in = any([words_not_search in titles[titles.index(
                                item)].upper() for words_not_search in words_not_searchs])

                            if word_key_not_in:
                                print('*************--- NOT SAVE ---*************')
                            else:
                                print('*************--- SAVE ---*************')
                                split_date = dates[titles.index(
                                    item)].rstrip().split('-')
                                dates_save = f"{split_date[0]} - {split_date[1]}"
                                link = f"https://rds-empleos.hn/plazas/category/17/{links_webs[titles.index(item)]}"

                                tenders_save = Tender(
                                    country_id=item_get_webs.country_id, profile_id=item_profile.id, description=titles[titles.index(item)], link=link, place_of_execution=places[titles.index(item)].rstrip(), awarning_authority=companies[titles.index(item)], dates=dates_save)
                                tenders_save.save()

        if len(emails_users) > 0:
            mailer.send(to=emails_users,
                        subject="Nuevas licitaciones", body="El sistema ha registrado nuevas licitaciones")
