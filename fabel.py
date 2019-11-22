import requests
from selenium import webdriver
import time


class Info:
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
    headers_simtech = {'Host': 'www.similartech.com',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                       'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'X-Request-Verification-Token': '4YeaXpHX1rFw1oKCN829peecJu8cjzJNZcqjYvQaFCkb4_hDOW2X0kAy1YoVH5Q5x0ckkJh8Q1C9t-zsv-sYIaeyp50X09CYp4szGfYu6fs7H3Ya0',
                       'X-Requested-With': 'XMLHttpRequest',
                       'DNT': '1',
                       'Connection': 'keep-alive',
                       'Referer': 'https://www.similartech.com/dashboard/websites/analysis/url/techrepublic.com'}
    cookies_simtech = {"__distillery": "2c36423_57e4dbce-cfb6-446e-8db8-4ad05dbd64c8-b7b3e61b3-b9b74ad8366e-afba",
                       "__hssrc": "1",
                       "__hstc": "34316798.cbf652281ed1486ead350d2d20713d40.1573885482404.1574210038208.1574281140622.5",
                       "__RequestVerificationToken": "8KNxCnz-fxaVsGMstSOpp7GIuz1LVSXVK5fX32UZUXAwmZP0UXVcvfUgWRxGQInJpGfD7V7tpC-YqtTpZRqHywtcbhE1",
                       "_fbp": "fb.1.1573885444745.1391239051", "_ga": "GA1.2.2065115807.1573885476", "_gat": "1",
                       "_gid": "GA1.2.1792528731.1574074480",
                       "_lr_hb_-eiz3eg/similartech": "{\"heartbeat\":1574341201095}",
                       "_lr_tabs_-eiz3eg/similartech": "{\"sessionID\":0,\"recordingID\":\"2-b9d44839-afc4-4f9f-bfe2-45832266c5df\",\"lastActivity\":1574341201093}",
                       "_lr_uf_-eiz3eg/similartech": "4a55cc01-e44a-4bae-b3bf-e7cfbb380710",
                       ".SAUTH": "3735B63A0D54E5C903E638F4DB1205EC4D1589683AB6E31F6619BE7C934899855DEC68E6567AEB0E1C98E3BFA426A9F6137342F4B1F20AB2D097DE6A6B3BB11B7E40EC03A4DCDEC1A74E0E303C70CDE3119F60DF88B067C338B99FB8AB7F9DF43661B025B91A8D68744E5F07DB099F74C464C6C68CCA5AF5F05D0CB508B199205FF62CF1AD239A1175A412B2F8D9DAB5A81C243C",
                       "cookieconsent_status": "dismiss", "hsfirstvisit": "",
                       "hubspotutk": "cbf652281ed1486ead350d2d20713d40",
                       "initialLP": "/dashboard/technologies/reports?callback=joined", "initialReferrer": "",
                       "intercom-session-v16ho3zr": "cGFtRWprR01ERWxHd05Ya3N1WWNVZjF1aWQ5eGppRFpEbEUvaExBdC91cGgwbEI0UitnR0ZOVDNOTS9vcFpTOS0tbld2OVg4NlhMdzN5TDJsMnFlWXdPQT09--088029f54d7437b13d22309efa0e203bdfc8646b",
                       "sessionLP": "/account/activate?email=tixet35697@3mailapp.net&token=Fl9t0Vs1gVlJ7zmrQtQkgwxpq6DErkttRiqodrp30601&utm_source=membership&utm_medium=email&utm_campaign=welcome&guidance=on",
                       "sessionReferrer": "https://temp-mail.org/ru/", "SGSS": "f3430786-2712-42aa-9966-8756b2680755",
                       "utm_campaign": "welcome", "utm_source": "membership"}

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


class Error(Exception):
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
                            raise Error("I found the Adsense in the Added")
                count = len(response.json()['alerts'][i]['removed'])
                if count > 0:
                    for y in range(count):
                        if response.json()['alerts'][i]['removed'][y]['id'] == 237:
                            # print(response.json()['alerts'][i]['date'] + ' removed')
                            flag = False
                            raise Error("I found the Adsense in the Removed")
        except Error as er:
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
        for i in range(54090, len(sites)):
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


path = Path()
info = Info()

main()
