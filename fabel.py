import re
import smtplib
import sys
import time

import dns.resolver
import mysql.connector
import requests
from bs4 import BeautifulSoup as bs
from mysql.connector import Error as MysqlError
from selenium import webdriver


class DataBase:
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
            sql_query = "INSERT INTO " + str(self._table) + " (domain) VALUES (%s)"
            cursor_db.execute(sql_query, (str(value).lower(),))
            connector_db.commit()
            return True
        except (mysql.connector.errors.IntegrityError, mysql.connector.errors.DataError) as er:
            print(er)


    def insert_into_db(self, column, domain, value):
        try:
            connector_db = self._connect_to_db()
            cursor_db = connector_db.cursor()
            sql_query = "UPDATE " + str(self._table) + " SET " + column + " = %s WHERE domain LIKE %s"
            cursor_db.execute(sql_query, (value, str(domain).lower(),))
            connector_db.commit()
        except mysql.connector.errors.DatabaseError as er:
            print(er)
        return 0

    def select_from_db(self, columns, requirement):
        connector_db = self._connect_to_db()
        cursor_db = connector_db.cursor()
        result = None
        try:
            sql_query = "SELECT " + columns + " FROM " + str(self._table) + " " + requirement
            print(sql_query)
            cursor_db.execute(sql_query)
            result = cursor_db.fetchall()
        except mysql.connector.errors.ProgrammingError as er:
            print(er)
        except mysql.connector.errors.InterfaceError as er:
            print(er)
        return result


class Website:
    def __init__(self):
        self._headers = {'accept': '*/*',
                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
        self._key_words = ['added', 'removed']
        self._adbrainer_url = 'https://dashboard.adbrainer.com/main/dashboard?token=f0fe34639af4c2587ec33f37346e15ba'
        self._bad_mail_names = ['abuse', 'noreply', 'no-reply', 'legal']
        self.simtech_headers = {'Host': 'www.similartech.com',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                                'Accept': 'application/json, text/javascript, */*; q=0.01',
                                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'X-Request-Verification-Token': 'X2qk4AHaWfbjjO4s6Uf4eaVg_sYAbzXl-6ovymkHgFfuZetIIOWoJHV3GP0WheB1gzKGViPxfifNaLiy4a5EcGSNiO5AKqeQZ_NTNa60p0gnWZH90',
                                'X-Requested-With': 'XMLHttpRequest',
                                'DNT': '1',
                                'Connection': 'keep-alive',
                                'Referer': 'https://www.similartech.com/dashboard/websites/analysis/url/techrepublic.com'}
        self.simtech_cookies = {"__hssrc": "1",
                                "__hstc": "34316798.4d8d3c8da67a33806ba839b1cf7689b6.1577938482158.1577938482158.1578007635585.2",
                                "__RequestVerificationToken": "44mht-8bgMtTPwsf7oJB2hVVp9k5U0KBKm9V2LCvuV3pLPXbGNZtjCpVIJWkdN5VdMBynhxP05LYjPgnQCcziGKxspQ1",
                                "_fbp": "fb.1.1577938431307.1703082896", "_ga": "GA1.2.492578486.1577938481",
                                "_gat": "1", "_gid": "GA1.2.1099574951.1577938481",
                                "_lr_hb_-eiz3eg/similartech": "{\"heartbeat\":1578010337216}",
                                "_lr_tabs_-eiz3eg/similartech": "{\"sessionID\":0,\"recordingID\":\"3-734dac71-1bd1-43da-924c-3e732576a06f\",\"lastActivity\":1578010337215}",
                                "_lr_uf_-eiz3eg/similartech": "a09affd6-d1a0-4d8b-a53a-fc9a4aa3e663",
                                ".SAUTH": "5FF47892A4C14B87CF2A75A96B430B7230C951594425D2226752D2B0C3460E5B68292660197440C8F6F85A133A6FB2D144DD232AA17BD6126DCB5713D63F29E24305538E0411D6684101B84DE96666086197B76C142A887BF40E8822497303D11BB5AE58E30D84B525DC90AF76CF363751E4539E87001EE9BDD8E4634B18304582609FA096025A417C4D4B8C0FA081FCC9332CFF",
                                "cookieconsent_status": "dismiss", "hsfirstvisit": "",
                                "hubspotutk": "4d8d3c8da67a33806ba839b1cf7689b6",
                                "initialLP": "/dashboard/technologies/reports?callback=joined", "initialReferrer": "",
                                "intercom-session-v16ho3zr": "TU9pMStBTmtxSEpVeWkyanIxemE4aktEcDRlZ0krNEhzZHpoZCtUZXozNGJJVG96NllaQjZYekM2cjlsY21scC0tekVvaTFOdE5JWWI1VjhUWVJqeG5NZz09--0191cd9df68995046001382126a146f76c98a965",
                                "sessionLP": "/dashboard/technologies/reports?callback=joined", "sessionReferrer": "",
                                "SGSS": "b6c18723-3b81-4e75-9818-c2dc5ffa58f9"}
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
            print(er)

    @staticmethod
    def get_monthly_visits(response):
        month_visits = response.json()['discover']['info']['monthlyVisits']
        return month_visits

    def get_emails(self, response):
        try:
            emails = response.json()['discover']['emails']['roleBasedEmails']
            emails = [emails[i] for i in range(len(emails)) if i < 7 and emails[i].split('@')[0] not in self._bad_mail_names]
            return emails
        except (ValueError, KeyError) as er:
            print(er)
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

    @staticmethod
    def check_existence_in_adbrainer(web_driver, domain):
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
                print(er)
                return False
            except Exception as er:
                print(er)
                # web_driver.quit()
                # break


class Email(Website):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self._base_email_address = 'corn@bt.com'
        self._domain_extensions = ['/about', '/about-us', '/contact', '/contact-us', '/advertise', '/contacto', '/privacy-policy', '/privacy']

    @staticmethod
    def _get_mx_record(domain):
        try:
            records = dns.resolver.query(domain, 'MX')
            mx_record = str(records[0].exchange)
            return mx_record
        except Exception as er:
            print(er)

    def _smtp_query(self, server, mx_record, email_address):
        try:
            server.connect(mx_record)
            server.helo(server.local_hostname)  # server.local_hostname(Get local server hostname)
            server.mail(self._base_email_address)
            code, message = server.rcpt(email_address)
            server.quit()
            return code
        except Exception as er:
            print(er)

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
            print(er)

    @staticmethod
    def _analyze_tag_a(tag):
        tag = tag.get('href')
        if tag is not None:
            text = str(tag.encode('utf-8'))
            result = re.findall(r"(?i)(http.+[\w\d].(contact|about|privacy).+[\w\d])", text)
            if result:  # len(result) > 0
                return result[0][0]

    def _find_links_on_page(self, response):
        links = []
        soup = bs(response, 'lxml')
        tag_a = soup.find_all('a')
        for i in range(len(tag_a)):
            link = self._analyze_tag_a(tag_a[i])
            if link not in links and link is not None:
                links.append(link.replace('https', 'http'))
        return links

    @staticmethod
    def _check_email_matching(email, domain):
        domain = str(re.findall(r"[+\w-]+", domain)[0])
        if email.find(domain) != -1:
            return True

    def _find_email_address(self, text, domain):
        result = []
        emails = re.findall(r"[.\w\-+]+@[\w\-+]+\.(?!png)[.\w]+", text)
        for i in range(len(emails)):
            if emails[i] not in result and self._check_email_matching(emails[i], domain) is True:
                result.append(emails[i])
        return result

    def _parse_page(self, response, domain):
        soup = (bs(response, 'lxml')).encode('utf-8')
        emails = self._find_email_address(str(soup), domain)
        if len(emails) > 0:
            return emails

    def search_email(self, domain):
        response = self.request(domain, self._headers, '')
        print(response.encoding)
        if response:
            emails = self._parse_page(response.content, domain)
            if emails:
                self.database.insert_into_db('emails', domain, ' '.join(emails))
            else:
                links = self._find_links_on_page(response.content) + [domain + self._domain_extensions[i] for i in range(len(self._domain_extensions))]
                for link in links:
                    response = self.request(link, self._headers, '')
                    if response:
                        emails = self._parse_page(response.content, domain)
                        if emails:
                            self.database.insert_into_db('emails', domain, ' '.join(emails))


class Advertisement:
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
                print(er)
                flag = 'error click'
        return flag

    def find_advertisement(self, web_driver, domain):
        try:
            web_driver.get('http://' + domain)
            time.sleep(4)
            iframes = web_driver.find_elements_by_tag_name('iframe')
            result = self._analyze_iframes(iframes)
            self._update_advertisement_info(domain, result)
        except Exception as er:
            print(er)

    def _update_advertisement_info(self, domain, result):
        if result == 'asw':
            self.database.insert_into_db('googleads', domain, 'y')
        elif result == 'google ads' or result == 'error click':
            self.database.insert_into_db('status', domain, 'needs to be checked again')
        elif result == 'no google ads':
            self.database.insert_into_db('status', domain, 'blocked')

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
                                                             "advertising = 'n' and "
                                                             "status = 'unchecked' and "
                                                             "monthly_visits = 'undefined' "
                                                             "LIMIT 20000")]
    for i in range(len(domains)):
        response = website.request(website.simtech_ajax_url + domains[i], website.simtech_headers, website.simtech_cookies)
        print(domains[i])
        print(response.content)
        if response:
            if website.get_monthly_visits(response) > 20000:
                db.insert_into_db('monthly_visits', domains[i], 'more_20thnd')
                if website.check_existence_in_adbrainer(adbrainer_web_driver, domains[i]) is True:
                    advert = website.get_advertising(response)
                    if advert:
                        if advert[0] == 'added':
                            db.insert_into_db('advertising', domains[i], 'y')
                            emails = website.get_emails(response)
                            valid_emails = [email for email in emails if mail.validate_email(email) == 250]
                            if valid_emails:
                                db.insert_into_db('emails', domains[i], ' '.join(valid_emails))
                            advrtsmnt.find_advertisement(advertisement_web_driver, domains[i])
                            if i % 100 == 0:
                                advrtsmnt.clear_tabs(advertisement_web_driver)
                        elif advert[0] == 'removed':
                            db.insert_into_db('advertising', domains[i], 'removed')
                    else:
                        db.insert_into_db('status', domains[i], 'blocked')
                else:
                    db.insert_into_db('status', domains[i], 'blocked')
            else:
                db.insert_into_db('monthly_visits', domains[i], 'less_20thnd')
        else:
            db.insert_into_db('existence', domains[i], 'n')
            db.insert_into_db('status', domains[i], 'blocked')
    advertisement_web_driver.quit()
    adbrainer_web_driver.quit()


if __name__ == '__main__':
    # main()
    def load_new_domains():
        db = DataBase('localhost', 'root', 'root01', 'fabel', 'domains')
        with open('./src/trash/loaded.txt') as f:
            for line in f:
                if db.insert_new_domain(line.strip().lower()):
                    print(line.strip().lower())
    load_new_domains()
# def update_info():
#     db = DataBase('localhost', 'root', 'root01', 'fabel')
#     with open('./src/trash/loaded.txt') as f:
#         for line in f:
#             db.insert_into_db('status', line.strip(), 'loaded')


