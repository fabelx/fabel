import requests
from selenium import webdriver
import time
import mysql.connector
from mysql.connector import Error


# Gold version 1.0.3


class DataBase:
    def __init__(self, host, user, password, database):
        self._host = host
        self._user = user
        self._password = password
        self._database = database

    def connect_to_db(self):
        connector_db = None
        try:
            connector_db = mysql.connector.connect(
                host=self._host,
                user=self._user,
                passwd=self._password,
                database=self._database
            )
        except Error as er:
            print(er)
        return connector_db

    def insert_new_domain(self, connector_db, value):
        try:
            cursor_db = connector_db.cursor()
            sql_query = "INSERT INTO domains (domain) VALUES (%s)"
            cursor_db.execute(sql_query, (str(value).lower(),))
            connector_db.commit()
        except mysql.connector.errors.IntegrityError as er:
            print(er)
        except mysql.connector.errors.DataError as er:
            print(er)
        return 0

    def insert_into_db(self, connector_db, column, domain, value):
        try:
            cursor_db = connector_db.cursor()
            sql_query = "UPDATE domains SET " + column + " = %s WHERE domain = %s"
            cursor_db.execute(sql_query, (value, str(domain).lower(),))
            connector_db.commit()
        except mysql.connector.errors.DatabaseError as er:
            print(er)
        return 0


# db = DataBase('localhost', 'root', 'root01', 'fabel')
# connector_db = db.connect_to_db()
# if connector_db is not None:
#     with open('./src/lib/list_of_websites.txt') as f:
#         for line in f:
#             db.insert_new_domain(connector_db, line.strip())


class Info:
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
    headers_simtech = {'Host': 'www.similartech.com',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                       'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'X-Request-Verification-Token': 'atyVD7vDW6DetJMF7CNR5w_4KX0x987N8ENUm_WgSc1xtI7Zi-jFKsqbXgJ6sQ6ZJoyNOjhKv8cBM3Ya4aCbFnmgQCn67YkOuvMdOv8CEBiq8r0Z0',
                       'X-Requested-With': 'XMLHttpRequest',
                       'DNT': '1',
                       'Connection': 'keep-alive',
                       'Referer': 'https://www.similartech.com/dashboard/websites/analysis/url/techrepublic.com'}
    cookies_simtech = {"__hssc": "34316798.3.1577211617180", "__hssrc": "1",
                       "__hstc": "34316798.8fb01c1eb2f72727a9c4674b1250472f.1577211617179.1577211617179.1577211617179.1",
                       "__RequestVerificationToken": "T14gPSr5_V2hrEv9Y2HHM9xnlsaq6WRPsqbvoi5teQLxEdEChaDgRe4CTXMNihMCApYmz3J_0ZxZsEhLX-a4I0BJ2w81",
                       "_fbp": "fb.1.1577211617044.1275765947", "_ga": "GA1.2.502283780.1577211617", "_gat": "1",
                       "_gid": "GA1.2.1773445000.1577211617",
                       "_lr_hb_-eiz3eg/similartech": "{\"heartbeat\":1577211685905}",
                       "_lr_tabs_-eiz3eg/similartech": "{\"sessionID\":0,\"recordingID\":\"3-0975d0fc-17b6-4b4f-b5b5-d9ebab8bd78b\",\"lastActivity\":1577211685902}",
                       "_lr_uf_-eiz3eg/similartech": "85e94927-1a6e-445d-987e-5e83795536a2",
                       ".SAUTH": "59FFE4F54F76F1F1B736E90382E875FD6D1FC6ED030C52F32066D4639F64529FC496C5BC01C37FE5C3165EAEEA6D7FCA1A7B460EC386B875D8E6223448E04544ADF491E0ADC1D4FA3C22BE58738EC576663572574F212ED70D50FA7155B1134C05D9697FD29A065DC6714416F2B19E552EA39484902708065F47B7B64297D189F37848C25D8381E59840E14F3886705C0912F4D4",
                       "cookieconsent_status": "dismiss", "hsfirstvisit": "",
                       "hubspotutk": "8fb01c1eb2f72727a9c4674b1250472f",
                       "initialLP": "/account/login?ReturnUrl=/dashboard/websites/analysis/url/www.cnn.com",
                       "initialReferrer": "",
                       "intercom-session-v16ho3zr": "OTF1SXczZGh4eWowZ0FtZHFTcWw3aVI1VEZGRzVVNUlsVGdMUG0rWE5veUNZaTNEKzlpQUtrUkQxS0hJR09IZi0tNEZ1YXBCcmpGS0JUdkNhcmZTYnlDZz09--3a98f83de2ad6a3dd88379f5b70e07114792e8ed",
                       "sessionLP": "/account/login?ReturnUrl=/dashboard/websites/analysis/url/www.cnn.com",
                       "sessionReferrer": "", "SGSS": "61c9fb49-3d5c-4c64-8150-87507e9f76f2"}

    base_url = 'https://www.similartech.com/api/websites/analysis?site='
    adbrainer_url = 'https://dashboard.adbrainer.com/main/dashboard?token=f0fe34639af4c2587ec33f37346e15ba'
    symbols = (
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w',
        'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    email = ['none']


class Path:
    base_path = 'D:/Vlad/My Project/fabel/src'
    categories_path = base_path + '/base_src/categories.txt'
    sites_path = base_path + '/base_src/sites.txt'
    up_20k_path = base_path + '/trash/sites_more_2000.txt'
    done_path = base_path + '/done/done.txt'
    google_iframe = base_path + '/trash/google_iframe.txt'
    error_click = base_path + '/trash/error_click.txt'
    ads_path = base_path + '/ads/sites_with_ads.txt'
    num_path = base_path + '/buf/num.txt'


class Fake_error(Exception):
    def __init__(self, text):
        self.txt = text


def request(url, headers, cookies):
    session = requests.session()
    response = session.get(url, headers=headers, cookies=cookies)
    return response


def read_list(path):
    list_ = []
    with open(path) as f:
        for line in f:
            list_.append(line.strip().lower())
    return list_


def clear_tabs(driver):
    list_of_tabs = driver.window_handles
    current_tab = driver.current_window_handle
    if len(list_of_tabs) > 1:
        for i in range(1, len(list_of_tabs)):
            driver.switch_to.window(list_of_tabs[i])
            driver.close()
    driver.switch_to.window(current_tab)


def module_similar_tech(site):
    """ This module made for getting data from Similar Tech. Data: monthly visits; google adsense """

    def get_month_visits(response):
        month_visits = response.json()['discover']['info']['monthlyVisits']
        return month_visits

    def get_email(response, email):
        try:
            email = response.json()['discover']['emails']['roleBasedEmails']
        except ValueError and KeyError:
            pass
        return email

    def get_ads(response):
        flag = -1
        try:
            for i in range(len(response.json()['alerts'])):
                count = len(response.json()['alerts'][i]['added'])
                if count > 0:
                    for y in range(count):
                        if response.json()['alerts'][i]['added'][y]['id'] == 237:
                            # print(response.json()['alerts'][i]['date'] + ' added')
                            flag = True
                            raise Fake_error("I found the Adsense in the Added")
                count = len(response.json()['alerts'][i]['removed'])
                if count > 0:
                    for y in range(count):
                        if response.json()['alerts'][i]['removed'][y]['id'] == 237:
                            # print(response.json()['alerts'][i]['date'] + ' removed')
                            flag = False
                            raise Fake_error("I found the Adsense in the Removed")
        except Fake_error as er:
            print(er)
        return flag

    response = request(info.base_url + site, info.headers_simtech, info.cookies_simtech)
    # print(response.content)
    info_site_ads = []
    if response.status_code == 200:
        if int(get_month_visits(response)) > 20000:
            flag = get_ads(response)
            if flag == True:
                email = get_email(response, info.email)
                with open(path.ads_path, 'a') as f:
                    f.write(site)
                    info_site_ads.append(site)
                    for line in range(len(email)):
                        f.write(' ' + email[line])
                        info_site_ads.append(email[line])
                    f.write('\n')
    else:
        print('error response: {}'.format(str(response)))
    return info_site_ads


def module_accepter(driver, site):
    """ This module made for accepting of site in adbrainer database """

    flag = False
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="form_content"]').send_keys(site)
            driver.find_element_by_xpath('//*[@id="form_save"]').click()
            status = driver.find_element_by_xpath('/html/body/div[1]/div/form/div/span').text
            if status == 'Site ' + site + ' is ok!':
                flag = True
                break
            else:
                break
        except:
            driver.get(info.adbrainer_url)
            print('error')
    return flag


def module_iframe_finder(driver, site):
    """ This module made for finding iframe in a site """

    flag = 'no'
    try:
        driver.get('http://' + site)
        time.sleep(4)
        iframes = driver.find_elements_by_tag_name('iframe')
        for i in range(len(iframes)):
            try:
                iframe = iframes[i]
                id = str(iframe.get_attribute('id'))
                if id.find('aswift') != -1 and len(id) > 1:
                    iframe.click()
                    flag = 'aswift'
                    break
                if id.find('google_ads') != -1 and len(id) > 1:
                    iframe.click()
                    flag = 'google_ads'
                    break
            except:
                flag = 'error_click'
    except:
        print('error in module_iframe_finder')
    return flag


def main():
    driver_acceptor = webdriver.Firefox()
    driver_iframe_finder = webdriver.Firefox()
    driver_acceptor.get(info.adbrainer_url)
    sites = read_list(path.sites_path)
    try:
        for i in range(9237, len(sites)):
            print(str(i) + ' ' + info.base_url + sites[i])
            site_ads = module_similar_tech(sites[i])
            if len(site_ads) != 0 and site_ads[1] != 'none':
                flag_accept = module_accepter(driver_acceptor, site_ads[0])
                if flag_accept == True:
                    flag_iframe = module_iframe_finder(driver_iframe_finder, site_ads[0])
                    if flag_iframe == 'aswift':
                        with open(path.done_path, 'a') as f:
                            for y in range(len(site_ads)):
                                f.write(str(site_ads[y]) + ' ')
                            f.write('\n')
                    elif flag_iframe == 'google_ads':
                        with open(path.google_iframe, 'a') as f:
                            for y in range(len(site_ads)):
                                f.write(str(site_ads[y]) + ' ')
                            f.write('\n')
                    elif flag_iframe == 'error_click':
                        with open(path.error_click, 'a') as f:
                            for y in range(len(site_ads)):
                                f.write(str(site_ads[y]) + ' ')
                            f.write('\n')
            if i % 100 == 0:
                clear_tabs(driver_iframe_finder)
                print('')
    except:
        driver_iframe_finder.quit()
        driver_acceptor.quit()


path = Path()
info = Info()

# main()
