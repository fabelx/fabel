from selenium import webdriver
import keyboard
# D:\Vlad\My Project\fabel\src\adbr_accept_src\adbrainer_accept_with_email.txt
# D:\Vlad\My Project\fabel\src\done\main_list.txt
def read_list(path):
    list_ = []
    with open(path) as f:
        for line in f:
            list_.append(line.strip().lower())
    return list_


def module_fabel():
    urls = read_list(input('Enter path to source list of sites:').replace('\\', '/'))
    range_num_first = int(input('Enter start point:'))
    driver = webdriver.Firefox()
    try:
        for i in range(range_num_first, len(urls)):
            url = urls[i].split(' ')
            driver.get('http://' + url[0])
            while True:
                if keyboard.read_key() == 's':
                    with open('./src/ready_to_load.txt', 'a') as f:
                        f.write(urls[i] + '\n')
                    break
                elif keyboard.read_key() == 'space':
                    break
    except:
        pass
    driver.quit()


module_fabel()




# import requests
# import json
#
#
# class Info:
#     headers_simtech = {'Host': 'www.similartech.com',
#                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
#                'Accept': 'application/json, text/javascript, */*; q=0.01',
#                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#                'Accept-Encoding': 'gzip, deflate, br',
#                'X-Request-Verification-Token': 'z-xiyq6IW8BEoIzxoLCe6giYtDZWiU2a1XASJw1RbtZqwbpWiRXQK2_ts3MDHBqjys8SYynXl_xGmm0Ljnt1Bxg5Pcx6GV5-Kzj0VMEQJw4LoQZl0',
#                'X-Requested-With': 'XMLHttpRequest',
#                'DNT': '1',
#                'Connection': 'keep-alive',
#                'Referer': 'https://www.similartech.com/dashboard/websites/analysis/url/techrepublic.com'}
#     cookies_simtech = {"__hssc": "34316798.2.1573760613127", "__hssrc": "1",
#                "__hstc": "34316798.1f58c39294a7ee39d14952b9f16b0aae.1573583189428.1573743867076.1573760613127.4",
#                "__RequestVerificationToken": "6D4Ze84qZG0qxVQD1_AIiR4aO6TDInm0E4xDvH2FeYUdNdHz918F7orcFXf8p49_Q5HzM9urIMlTWn68UTTItB_D4d41",
#                "_fbp": "fb.1.1573583179652.1926837112", "_ga": "GA1.2.1958359811.1573583179", "_gat": "1",
#                "_gid": "GA1.2.1507809470.1573682052",
#                "_lr_hb_-eiz3eg/similartech": "{\"heartbeat\":1573760632063}",
#                "_lr_tabs_-eiz3eg/similartech": "{\"sessionID\":1,\"recordingID\":\"2-f60dcd92-107c-48b3-9fc7-a9d3257e6cf5\",\"lastActivity\":1573760632061}",
#                "_lr_uf_-eiz3eg/similartech": "42c8fc81-f2b7-43cc-9ef9-a13b701d3d63",
#                ".SAUTH": "0DC589A371237B7DA1FD4F01C838C824B50152104FD5D0E549DEF415E090832C984BCDEE2F0998E745EED3F227BDE01D3C0DC4D9DBBC5C78D5C92C62B7F5343535DD78BC4EF55D4EE5B857FC56C41D00A8CFF59ABEDB5257D77CFA082503AC43BC08168B1B5E3D6DEC72A82324D9C415D0EC3E54B4A4BF1D096109AFBB5E19A61BF177C0377CC1EC67CC60DB7E93B62533F5440F",
#                "cookieconsent_status": "dismiss", "hsfirstvisit": "",
#                "hubspotutk": "1f58c39294a7ee39d14952b9f16b0aae", "initialLP": "/account/register",
#                "initialReferrer": "",
#                "intercom-session-v16ho3zr": "UElENHh6T01TL2lERklSTXU4aVFRdkd6dGY5alNxSjlHWUxmM044OElBS2ZGS1FKZWw1akhxaGVMN1BqbElUai0tbjJCVC84UytBQkFLbzVISVorM3REdz09--8c219e87d2f80aa8de477889f7aec6eac508fb5c",
#                "sessionLP": "/account/register", "sessionReferrer": "",
#                "SGSS": "5614af80-6ce2-4b90-9e1e-a0a799dab169"}
#     base_url = 'https://www.similartech.com/api/websites/analysis?site='
#     symbols = (
#         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
#         'w',
#         'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
#     email = ['none']
#
#
# class Path:
#     base_path = 'D:/Vlad/My Project/fabel/src'
#     categories_path = base_path + '/base_src/categories.txt'
#     sites_path = base_path + '/base_src/sites.txt'
#     up_20k_path = base_path + '/trash/sites_more_2000.txt'
#
#
#
# class Error(Exception):
#     def __init__(self, text):
#         self.txt = text
#
#
# path = Path()
# info = Info()
#
#
# def request(url, headers, cookies):
#     session = requests.session()
#     response = session.get(url, headers=headers, cookies=cookies)
#     return response
#
#
# def read_list(path):
#     list_ = []
#     with open(path) as f:
#         for line in f:
#             list_.append(line.strip().lower())
#     return list_
#
#
# def module_similar_tech():
#     """ This module made for getting data from Similar Tech. Data: monthly visits; google adsense """
#
#     def get_month_visits(response):
#         month_visits = response.json()['discover']['info']['monthlyVisits']
#         return month_visits
#
#     def get_email(response, email):
#         try:
#             email = response.json()['discover']['emails']['roleBasedEmails']
#         except ValueError and KeyError:
#             pass
#         return email
#
#     def get_ads(response):
#         flag = ''
#         try:
#             for i in range(len(response.json()['alerts'])):
#                 count = len(response.json()['alerts'][i]['added'])
#                 if count > 0:
#                     for y in range(count):
#                         if response.json()['alerts'][i]['added'][y]['id'] == 237:
#                             # print(response.json()['alerts'][i]['date'] + ' added')
#                             flag = True
#                             raise Error("I found the Adsense in the Added")
#                 count = len(response.json()['alerts'][i]['removed'])
#                 if count > 0:
#                     for y in range(count):
#                         if response.json()['alerts'][i]['removed'][y]['id'] == 237:
#                             # print(response.json()['alerts'][i]['date'] + ' removed')
#                             flag = False
#                             raise Error("I found the Adsense in the Removed")
#         except Error as er:
#             print(er)
#         return flag
#
#     sites = read_list(path.sites_path)
#     for i in range(21439, len(sites)):
#         print(str(i) + '  https://www.similartech.com/dashboard/websites/analysis/url/' + sites[i])
#         response = request(info.base_url + sites[i], info.headers_simtech, info.cookies_simtech)
#         # print(response.content)
#         if response.status_code == 200:
#             # with open('data1.json', 'w') as f:
#             #     json.dump(response.json(), f)
#             if int(get_month_visits(response)) > 20000:
#                 flag = get_ads(response)
#                 if flag == True:
#                     email = get_email(response, info.email)
#                     with open('./src/ads/sites_with_ads.txt', 'a') as f:
#                         f.write(sites[i])
#                         for line in range(len(email)):
#                             f.write(' ' + email[line])
#                         f.write('\n')
#                 elif flag == False:
#                     email = get_email(response, info.email)
#                     with open('./src/ads/sites_with_ads_removed.txt', 'a') as f:
#                         f.write(sites[i])
#                         for line in range(len(email)):
#                             f.write(' ' + email[line])
#                         f.write('\n')
#                 elif flag == '':
#                     email = get_email(response, info.email)
#                     with open('./src/ads/sites_more_2000.txt', 'a') as f:
#                         f.write(sites[i])
#                         for line in range(len(email)):
#                             f.write(' ' + email[line])
#                         f.write('\n')
#         else:
#             print('error response: {}'.format(str(response)))
#
#
# def main():
#     module_similar_tech()
#
#
# main()
