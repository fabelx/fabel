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
                       'X-Request-Verification-Token': 'bUWOpt9OrQVwizrAQnVwz03RHTfO5V-Sdja8p_o65SBgouiRnjl1GSBJfgAHTa4zizQd-tgLvf0mjt00DIrVohs6zZUrCxy83SeTCU8CpRx_nRBU0',
                       'X-Requested-With': 'XMLHttpRequest',
                       'DNT': '1',
                       'Connection': 'keep-alive',
                       'Referer': 'https://www.similartech.com/dashboard/websites/analysis/url/techrepublic.com'}
    cookies_simtech = {"__hssc": "34316798.1.1574880032305", "__hssrc": "1",
                       "__hstc": "34316798.9b887398279677df0f007dee45c44667.1574693381336.1574693381336.1574880032305.2",
                       "__RequestVerificationToken": "imXVBryPoQaU0IF2zfna9HRWP4Ytucs-OArAxoCKd945dPG6_2wyD3jNPiQ0J_xOvRVSv6DvdOk3U5AsOgASMH20j3s1",
                       "_fbp": "fb.1.1574693368403.1205247694", "_ga": "GA1.2.1384714940.1574693378", "_gat": "1",
                       "_gid": "GA1.2.1229183313.1574880028",
                       "_lr_hb_-eiz3eg/similartech": "{\"heartbeat\":1574880049408}",
                       "_lr_tabs_-eiz3eg/similartech": "{\"sessionID\":0,\"recordingID\":\"2-85f9083d-7c5f-46f1-9bbf-74f1b7e04995\",\"lastActivity\":1574880049406}",
                       "_lr_uf_-eiz3eg/similartech": "457dc9a2-4431-4f1d-9fc6-26dcc6d9538e",
                       ".SAUTH": "1BC1D0E00C3F09D6C4A230616570AEF93588F7CE0291163962E9F82EBB7EB556A75181FFE61298A0485A58A7E71848D80D63C23BB3FB46FDF02CE2432335A85C6C6665E83785487A46D81DAF634781740F599A5AFBA49D0ACBCDD570CC47017B2A202D8A06599B587C220D8AC75D2341B8A3C646D75825B695ABB1D3E423AA2B7C2604DCE60902391C782B03F76EB02909AD777D",
                       "cookieconsent_status": "dismiss", "hsfirstvisit": "",
                       "hubspotutk": "9b887398279677df0f007dee45c44667", "initialLP": "/account/register",
                       "initialReferrer": "",
                       "intercom-session-v16ho3zr": "aGRCMzRMVmdQOGtnUW9uM2RTYVNSelZSN3h3S25uNUYxMjZNNG1sRHBZOGlCRlBmWkVpRnNjNEM2NW53SGpZbS0tclBQNXdmTHNFTlA0NlNiay96Tlhmdz09--ecde84f59dae77b727fa4cbc9eefe11a20afc405",
                       "sessionLP": "/account/register", "sessionReferrer": "",
                       "SGSS": "a4c9f75f-42fa-4ed2-92ad-d7f9e1925a07"}

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
        for i in range(len(sites)):
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

main()
