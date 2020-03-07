import logging
import smtplib
import sys
import time

import dns.resolver
import mysql.connector
import requests
from mysql.connector import Error as MysqlError
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException  # NoSuchWindowException

logger = logging.getLogger('fabel_logger')
console_handler = logging.StreamHandler()
logger_form = logging.Formatter(fmt='{asctime}    :    {lineno}   :   {funcName}     :    {message}', style='{')
logger.setLevel('ERROR')
logger.addHandler(console_handler)
console_handler.setFormatter(logger_form)


class DataBase:
    __slots__ = ('_host', '_user', '_password', '_database', '_table',)

    def __init__(self, host, user, password, database, table):
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._table = table

    def _connect_to_db(self):
        try:
            connector_db = mysql.connector.connect(
                host=self._host,
                user=self._user,
                passwd=self._password,
                database=self._database
            )
            return connector_db
        except MysqlError as er:
            print('Fatal error ' + str(er))
            sys.exit()

    def insert_new_domain(self, value):
        try:
            connector_db = self._connect_to_db()
            cursor_db = connector_db.cursor()
            sql_query = "INSERT INTO {} (domain) VALUES %s".format(str(self._table))
            cursor_db.execute(sql_query, (str(value).lower(),))
            connector_db.commit()
            return True
        except (mysql.connector.errors.IntegrityError, mysql.connector.errors.DataError) as er:
            logger.error(er)

    def insert_into_db(self, column, domain, value, requirement):
        try:
            connector_db = self._connect_to_db()
            cursor_db = connector_db.cursor()
            sql_query = "UPDATE {} SET {} = %s WHERE domain LIKE %s {}".format(str(self._table), column, requirement)
            cursor_db.execute(sql_query, (value, str(domain).lower(),))
            connector_db.commit()
        except mysql.connector.errors.DatabaseError as er:
            logger.error(er)
        return 0

    def select_from_db(self, columns, requirement):
        connector_db = self._connect_to_db()
        cursor_db = connector_db.cursor()
        result = None
        try:
            sql_query = "SELECT {} FROM {} {}".format(columns, str(self._table), requirement)
            cursor_db.execute(sql_query)
            result = cursor_db.fetchall()
        except mysql.connector.errors.ProgrammingError as er:
            print(er)
        except mysql.connector.errors.InterfaceError as er:
            print(er)
        return result


class Website:
    __slots__ = ('_headers', '_key_words', '_country_flags', '_adbrainer_url', '_bad_mail_names', 'simtech_headers',
                 'simtech_cookies', 'simtech_ajax_url', '_bad_country_flags',)

    def __init__(self):
        self._headers = {'accept': '*/*',
                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
        self._key_words = ('added', 'removed',)
        self._country_flags = ('UK', 'US', 'CA', 'AU', 'NZ',)
        self._bad_country_flags = ('CN', 'BD',)
        self._adbrainer_url = 'https://dashboard.adbrainer.com/main/dashboard?token=f0fe34639af4c2587ec33f37346e15ba'
        self._bad_mail_names = ('abuse', 'noreply', 'no-reply', 'legal',)
        self.simtech_headers = {'Host': 'www.similartech.com',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                                'Accept': 'application/json, text/javascript, */*; q=0.01',
                                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'X-Request-Verification-Token': 'JRRUwY6F9Dt-tDGd9WYmrhDOGwaYX7zfo10NNsdq08TCxmfVVLXoBxyMhrejZWW7ZAt2ZNbGp86QS_k14AUcDjzbcR4aCMHPdLyzq-Lbsx5V3m0n0',
                                'X-Requested-With': 'XMLHttpRequest',
                                'DNT': '1',
                                'Connection': 'keep-alive',
                                'Referer': 'https://www.similartech.com/dashboard/websites/analysis/url/techrepublic.com'}
        self.simtech_cookies = {"__hssc": "34316798.4.1582931738811", "__hssrc": "1",
                                "__hstc": "34316798.216d97b46808af3d69aeef29dde0d74a.1582931738811.1582931738811.1582931738811.1",
                                "__RequestVerificationToken": "k-F4nWsmicPA_xC6xgOxnOtFFZ9DuhpfKUqP50dz5T-ME98kOde_KHsp0o6cOlN6PcCpVUjvRIC1RWWqY-0xyW4pzkw1",
                                "_ga": "GA1.2.1975797809.1582931738", "_gat": "1", "_gid": "GA1.2.567801510.1582931738",
                                ".SAUTH": "F8B699DFC4504369102396CCC68192EE289F31519C31D0C8F481B6D1D92771257CC5882561FF77D948D636235F1C2FB79071865DA40601B894AB56FCF6E609B38FE3A929A36FFB83B9876B9B1C965DA593644F2C1DCC4890D7BF71ADD6738DEA4C587269BFDF2377211D650A81FA69AE327446615C1F9AAD0650666BFC2FD46DC23E00DC9FCC741CA61ECD2D21671D6352FA0DD6",
                                "cookieconsent_status": "dismiss", "hsfirstvisit": "",
                                "hubspotutk": "216d97b46808af3d69aeef29dde0d74a", "initialLP": "/",
                                "initialReferrer": "", "sessionLP": "/", "sessionReferrer": "",
                                "SGSS": "e0e42fd7-a727-4f7b-9999-16256ffc9b06"}
        self.simtech_ajax_url = 'https://www.similartech.com/api/websites/analysis?site='

    @staticmethod
    def request(url, headers, cookies):
        if url.find('http://') == -1 and url.find('https://') == -1:
            url = 'http://' + url
        session = requests.session()
        try:
            response = session.get(url, headers=headers, cookies=cookies)
            return response
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, Exception) as er:
            logger.error(er)

    @staticmethod
    def get_monthly_visits(response):
        month_visits = response.json()['discover']['info']['monthlyVisits']
        print(str(month_visits))
        return month_visits

    def get_country_flag(self, database, response, domain):
        try:
            country_flag = response.json()['discover']['info']['countryFlag']
            if country_flag in self._country_flags:
                database.insert_into_db('country_flag', domain, 'y', '')
                return True
            if country_flag in self._bad_country_flags:
                return False
            return True
        except (ValueError, KeyError) as er:
            logger.error(er)
            return True

    @staticmethod
    def get_facebook_url(database, response, domain):
        try:
            facebook_url = response.json()['discover']['company']['facebookUrl']
            database.insert_into_db('facebook_url', domain, facebook_url, '')
        except (ValueError, KeyError) as er:
            logger.error(er)

    def get_emails(self, response):
        try:
            emails = response.json()['discover']['emails']['roleBasedEmails']
            emails = [emails[i] for i in range(len(emails)) if
                      i < 4 and emails[i].split('@')[0] not in self._bad_mail_names]
            return emails
        except (ValueError, KeyError) as er:
            logger.error(er)
            return []

    def _search_for_advert_data(self, data):
        result = []
        for key_word in self._key_words:
            count = len(data[key_word])
            if count > 0:
                if 237 in [data[key_word][i]['id'] for i in range(count) if data[key_word][i]['id'] == 237]:
                    result.append(key_word)
                    break
        return result

    def get_advertising(self, response):
        response = response.json()['alerts']
        try:
            for i in range(len(response)):
                result = self._search_for_advert_data(response[i])
                if len(result) > 0:
                    return result
        except KeyError as er:
            print("Didn't find: " + str(er))

    def run_web_driver_for_adbrainer(self):
        web_driver = webdriver.Firefox()
        web_driver.get(self._adbrainer_url)
        return web_driver

    def check_existence_in_adbrainer(self, web_driver, domain):
        while True:
            try:
                web_driver.find_element_by_xpath('//*[@id="form_content"]').send_keys(domain)
                web_driver.find_element_by_xpath('//*[@id="form_save"]').click()
                status = web_driver.find_element_by_xpath('/html/body/div[1]/div/form/div/span').text
                if status == 'Site ' + str(domain) + ' is ok!':
                    return True
                else:
                    return False
            except TypeError as er:
                logger.error(er)
                return False
            except NoSuchElementException as er:
                logger.error(er)
                web_driver.get(self._adbrainer_url)
            except Exception as er:
                logger.error(er, exc_info=True)
                sys.exit()

    def check_web_driver_existing(self, web_driver):
        try:
            if web_driver.window_handles:
                return web_driver
        except WebDriverException as er:
            logger.error(er)
            return self.run_web_driver_for_adbrainer()


class Email(Website):
    __slots__ = ('database', '_base_email_address', '_key_words',)

    def __init__(self, database):
        super().__init__()
        self.database = database
        self._base_email_address = 'gigini7709@mailmink.com'

    @staticmethod
    def _get_mx_record(domain):
        try:
            records = dns.resolver.query(domain, 'MX')
            mx_record = str(records[0].exchange)
            return mx_record
        except Exception as er:
            logger.error(er)

    def _smtp_query(self, server, mx_record, email_address):
        try:
            server.connect(mx_record)
            server.helo(server.local_hostname)  # server.local_hostname(Get local server hostname)
            server.mail(self._base_email_address)
            code, message = server.rcpt(email_address)
            server.quit()
            if str(message).lower().find('access denied') != -1 or str(message).lower().find('block') != -1:
                return 250
            else:
                return code
        except smtplib.SMTPServerDisconnected as er:
            logger.error(er)
            return 250
        except TimeoutError as er:
            logger.error(er)
            return 1000
        except Exception as er:
            logger.error(er, exc_info=True)
            return 400

    def validate_email(self, email_address):
        status_code = 400
        try:
            mail_name, domain = str(email_address).split('@')
            mx_record = self._get_mx_record(domain)
            if mx_record is not None:
                server = smtplib.SMTP()
                server.set_debuglevel(0)
                status_code = self._smtp_query(server, mx_record, email_address)
            return status_code
        except ValueError as er:
            logger.error(er)


class Advertisement:
    __slots__ = ('database',)

    def __init__(self, database):
        self.database = database

    @staticmethod
    def _analyze_iframes(iframes):
        flag = 'no google ads'
        for iframe in iframes:
            id_value = iframe.get_attribute('id')
            try:
                if id_value.find('aswift') != -1:
                    iframe.click()
                    flag = 'asw'
                    return flag
                elif id_value.find('google') != -1:
                    iframe.click()
                    flag = 'google ads'
                    return flag
            except Exception as er:
                logger.error(er)
                flag = 'error click'
        return flag

    def find_advertisement(self, web_driver, domain):
        try:
            web_driver.get('http://' + domain)
            time.sleep(4)
            iframes = tuple(web_driver.find_elements_by_tag_name('iframe'))
            result = self._analyze_iframes(iframes)
            self._update_advertisement_info(domain, result)
        except WebDriverException as er:
            logger.error(er)
            self.database.insert_into_db('existence', domain, 'n', '')
        except Exception as er:
            logger.error(er, exc_info=True)

    def _update_advertisement_info(self, domain, result):
        if result == 'asw':
            self.database.insert_into_db('googleads', domain, 'y', '')
        elif result == 'google ads' or result == 'error click':
            self.database.insert_into_db('status', domain, 'needs to be checked again', '')
        elif result == 'no google ads':
            self.database.insert_into_db('status', domain, 'blocked', '')

    @staticmethod
    def clear_tabs(web_driver):
        list_of_tabs = web_driver.window_handles
        current_tab = web_driver.current_window_handle
        if len(list_of_tabs) > 1:
            for i in range(1, len(list_of_tabs)):
                web_driver.switch_to.window(list_of_tabs[i])
                web_driver.close()
        web_driver.switch_to.window(current_tab)


def main():
    db = DataBase('localhost', 'root', 'root01', 'fabel', 'domains')
    website = Website()
    mail = Email(db)
    advrtsmnt = Advertisement(db)
    advertisement_web_driver = webdriver.Firefox()
    adbrainer_web_driver = mail.run_web_driver_for_adbrainer()
    domains = [row[0] for row in db.select_from_db('domain', "WHERE existence = 'y' and "
                                                             "status = 'unchecked' and "
                                                             "googleads = 'y' and "
                                                             "advertising = 'y' and "
                                                             "emails = 'none' "
                                                             "LIMIT 40000")]
    domains = tuple(domains)
    for i in range(len(domains)):
        while True:
            try:
                response = website.request('{}{}'.format(website.simtech_ajax_url, domains[i]), website.simtech_headers,
                                           website.simtech_cookies)
                print(domains[i])
                break
            except AttributeError as er:
                logger.error(er)
        if response:
            monthly_visits = website.get_monthly_visits(response)
            if monthly_visits > 100000 and website.get_country_flag(db, response, domains[i]):
                if 500000 > monthly_visits > 150000:
                    db.insert_into_db('monthly_visits', domains[i], 'more_150thnd', '')
                elif monthly_visits > 500000:
                    db.insert_into_db('monthly_visits', domains[i], 'more_500thnd', '')
                else:
                    db.insert_into_db('monthly_visits', domains[i], 'more_100thnd', '')
                adbrainer_web_driver = website.check_web_driver_existing(adbrainer_web_driver)
                if website.check_existence_in_adbrainer(adbrainer_web_driver, domains[i]) is True:
                    advert = website.get_advertising(response)
                    if advert:
                        if advert[0] == 'added':
                            db.insert_into_db('advertising', domains[i], 'y', '')
                            emails = website.get_emails(response)
                            # valid_emails = [email for email in emails if
                            #                 mail.validate_email(email) == 250 or mail.validate_email(email) == 451]
                            if emails:
                                db.insert_into_db('emails', domains[i], ' '.join(emails), '')
                            else:
                                website.get_facebook_url(db, response, domains[i])
                            advertisement_web_driver = website.check_web_driver_existing(advertisement_web_driver)
                            advrtsmnt.find_advertisement(advertisement_web_driver, domains[i])
                            if i % 100 == 0:
                                advrtsmnt.clear_tabs(advertisement_web_driver)
                        elif advert[0] == 'removed':
                            db.insert_into_db('advertising', domains[i], 'removed', '')
                    else:
                        db.insert_into_db('status', domains[i], 'blocked', '')
                else:
                    db.insert_into_db('status', domains[i], 'blocked', '')
            else:
                # db.insert_into_db('monthly_visits', domains[i], 'less_20thnd', '')
                db.insert_into_db('status', domains[i], 'blocked', '')
        else:
            db.insert_into_db('existence', domains[i], 'n', '')
            db.insert_into_db('status', domains[i], 'blocked', '')
    advertisement_web_driver.quit()
    adbrainer_web_driver.quit()


if __name__ == '__main__':
    main()
