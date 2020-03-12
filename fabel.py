# import typing
import json
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


def making_logger(handler, **kwargs):
    """Example: logger = making_logger('file or console', name='name of your logger', level=LEVEL, filename='example.log')"""
    if handler == 'console':
        my_handler = logging.StreamHandler()
    elif handler == 'file':
        my_handler = logging.FileHandler(kwargs['filename'])
    else:
        print("The handler value you entered is not valid. Valid values: console or file.")
        raise ValueError('handler = {}'.format(handler))
    logger_format = logging.Formatter(fmt='{asctime}  :  {lineno}  :  {funcName}  :  {message}', style='{')
    my_handler.setFormatter(logger_format)
    my_log = logging.getLogger(kwargs['name'])
    my_log.addHandler(my_handler)
    my_log.setLevel(kwargs['level'])
    my_log.propagate = False
    return my_log


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
            console_logger.critical('Fatal error ' + str(er))  # raise
            sys.exit()

    def insert_new_domain(self, value):
        try:
            connector_db = self._connect_to_db()
            cursor_db = connector_db.cursor()
            sql_query = f"INSERT INTO {self._table} (domain) VALUES ('{value.lower()}')"
            cursor_db.execute(sql_query, )
            connector_db.commit()
            return True
        except (mysql.connector.errors.IntegrityError, mysql.connector.errors.DataError) as er:
            file_logger.warning(
                f"An error occurred while adding a new domain in the database. Domain: {value}. Error: {er}")
            return False

    def insert_into_db(self, column, domain, value, requirement):
        try:
            connector_db = self._connect_to_db()
            cursor_db = connector_db.cursor()
            sql_query = "UPDATE {} SET {} = %s WHERE domain LIKE %s {}".format(str(self._table), column, requirement)
            cursor_db.execute(sql_query, (value, str(domain).lower(),))
            connector_db.commit()
        except mysql.connector.errors.DatabaseError as er:
            file_logger.warning(f"An insert error of value: {value} where domain is: {domain} Error: {er}")
            return False
        return 0

    def select_from_db(self, columns, requirements):
        connector_db = self._connect_to_db()
        cursor_db = connector_db.cursor()
        try:
            sql_query = f"SELECT {columns} FROM {self._table} {requirements}"
            cursor_db.execute(sql_query)
            result = cursor_db.fetchall()
            return result
        except mysql.connector.errors.ProgrammingError as er:
            file_logger.warning(er)
        except mysql.connector.errors.InterfaceError as er:
            file_logger.warning(er)


class Website:
    __slots__ = ('_headers', '_key_words', '_country_flags', '_adbrainer_url', '_bad_mail_names', 'simtech_headers',
                 'simtech_cookies', 'simtech_ajax_url', '_bad_country_flags',)

    def __init__(self):
        conf_data = self.__init_conf__()
        self._headers = conf_data['website']['headers']
        self._key_words = conf_data['website']['key_words']
        self._country_flags = conf_data['website']['country_flags']
        self._bad_country_flags = conf_data['website']['bad_country_flags']
        self._adbrainer_url = conf_data['website']['adbrainer_url']
        self._bad_mail_names = conf_data['website']['bad_mail_names']
        self.simtech_headers = conf_data['website']['simtech_headers']
        self.simtech_cookies = conf_data['website']['simtech_cookies']
        self.simtech_ajax_url = conf_data['website']['simtech_ajax_url']

    def __init_conf__(self):
        with open('conf.json', 'r') as f:
            return json.load(f)

    @staticmethod
    def request(url, headers, cookies):
        if url.find('http://') == -1 and url.find('https://') == -1:
            url = 'http://' + url
        session = requests.session()
        try:
            response = session.get(url, headers=headers, cookies=cookies)
            return response
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, Exception) as er:
            file_logger.warning(er)

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
            file_logger.warning(er)
            return True

    @staticmethod
    def get_facebook_url(database, response, domain):
        try:
            facebook_url = response.json()['discover']['company']['facebookUrl']
            database.insert_into_db('facebook_url', domain, facebook_url, '')
        except (ValueError, KeyError) as er:
            file_logger.warning(er)

    def get_emails(self, response):
        try:
            emails = response.json()['discover']['emails']['roleBasedEmails']
            emails = [emails[i] for i in range(len(emails)) if
                      i < 4 and emails[i].split('@')[0] not in self._bad_mail_names]
            return emails
        except (ValueError, KeyError) as er:
            file_logger.warning(er)
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
                file_logger.error(er)
                return False
            except NoSuchElementException as er:
                file_logger.error(er)
                web_driver.get(self._adbrainer_url)
            except Exception as er:
                file_logger.warning(er, exc_info=True)
                sys.exit()

    def check_web_driver_existing(self, web_driver):
        try:
            if web_driver.window_handles:
                return web_driver
        except WebDriverException as er:
            file_logger.error(er)
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
            file_logger.warning(er)

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
            file_logger.warning(er)
            return 250
        except TimeoutError as er:
            file_logger.warning(er)
            return 1000
        except Exception as er:
            file_logger.warning(er, exc_info=True)
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
            file_logger.warning(er)


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
                file_logger.warning(er)
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
            file_logger.warning(er)
            self.database.insert_into_db('existence', domain, 'n', '')
        except Exception as er:
            file_logger.warning(er, exc_info=True)

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
                console_logger.info(domains[i])
                break
            except AttributeError as er:
                file_logger.error(er)
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
                db.insert_into_db('status', domains[i], 'blocked', '')
        else:
            db.insert_into_db('existence', domains[i], 'n', '')
            db.insert_into_db('status', domains[i], 'blocked', '')
    advertisement_web_driver.quit()
    adbrainer_web_driver.quit()


if __name__ == '__main__':
    console_logger = making_logger('console', name='console_logger', level='INFO')
    file_logger = making_logger('file', name='file_logger', level='WARNING', filename='main_fabel.log')
    main()
