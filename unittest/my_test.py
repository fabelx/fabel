import sys
import os
import unittest
import requests
import json
from selenium import webdriver
import fabel
import time
from fabel import making_logger
sys.path.append(os.getcwd())




class TestDatabase(unittest.TestCase):
    def test_insert_domain(self):
        db = fabel.DataBase('localhost', 'root', 'root01', 'fabel', 'domains')
        self.assertEqual(db.insert_new_domain('deccoria.pl'), False)
        # self.assertEqual(db.insert_new_domain([44, 66]), False)


    def test_insert_into_db(self):
        db = fabel.DataBase('localhost', 'root', 'root01', 'fabel', 'domains')
        self.assertEqual(db.insert_into_db('googleads', 'deccoria.pl', 'o', ''), False)

    def test_select_from_bd(self):
        db = fabel.DataBase('localhost', 'root', 'root01', 'fabel', 'domains')
        self.assertEqual(db.select_from_db('domain', "WHERE domain LIKE '%.gov%' LIMIT 10"), [])


class TestWebsite(unittest.TestCase):
    pass

    # def test_request(self):
    #     website = fabel.Website()
    #     # self.assertEqual(website.request('google.com', ''), None)
    #     self.assertEqual(website.request('http://googlem', ''), None)
    #     # self.assertEqual(website.request('http://google.com', ''), 0)

    # def test_get_data(self):
    #     with open('D:/Vlad/My Project/fabel/src/trash/data.json') as f:
    #         data = json.load(f)
    #     website = fabel.Website()
    #     # self.assertEqual(website.get_monthly_visits(data), 6800000.0)
    #     # self.assertEqual(website.get_emails(data), ['career@techrepublic.com', 'netadmin@techrepublic.com',
    #     #                                             'support@techrepublic.com', 'supportrepublic@techrepublic.com'])
    #     # self.assertEqual(website.get_advertising(data), ['added'])
    #     # self.assertEqual(website.get_advertising(data), [])

    # def test_web_driver_for_checking_existence(self):
    #     website = fabel.Website()
    #     web_driver = website.run_web_driver_for_adbrainer()
    #     time.sleep(5)
    #     self.assertEqual(website.check_existence_in_adbrainer(web_driver, 'kkk'), None)
    #     # self.assertEqual(website.run_web_driver_for_adbrainer(), None)
    #     self.assertEqual(website.check_existence_in_adbrainer(web_driver, 'werhdtfgjhm'), True)
    #     self.assertEqual(website.check_existence_in_adbrainer(web_driver, 'mobtada.com'), False)
    #     self.assertEqual(website.check_existence_in_adbrainer(web_driver, 0), False)
    #     self.assertEqual(website.check_existence_in_adbrainer(web_driver, ['0', 0]), False)
    #     self.assertEqual(website.check_existence_in_adbrainer(web_driver, 'mobtada.com'), False)


class TestEmail(unittest.TestCase):
    pass
    # def test_validete(self):
    #     em = fabel.Email()
    #     # self.assertEqual(em.validate('daprostovseeto@gmail.com'), 250)
    #     # self.assertEqual(em.validate('editor@accountingweb.com'), 250)
    #     # self.assertEqual(em.validate('support@sinemanija.com'), 250)
    #     # self.assertEqual(em.validate('support@sinemanihsgdfjyhvhja.com'), 400)
    #     # self.assertEqual(em.validate('daprostovgrehdrfgseeto@gmail.com'), 250)
    #     self.assertEqual(em.validate(9), None)
    #     self.assertEqual(em.validate(['TTT', 9]), None)
    #     # self.assertEqual(em.validate('support@sinemanija.com'), 250)
    #     # self.assertEqual(em.validate('support@sinemanihsgdfjyhvhja.com'), 400)


class TestAdvertisement(unittest.TestCase):
    pass
    # def test_find_iframe(self):
    #     find_iframe_web_driver = webdriver.Firefox()
    #     fm = fabel.Advertisement('localhost', 'root', 'root01', 'fabel')
    #     self.assertEqual(fm.find_advertisement(find_iframe_web_driver, 'google.com'), None)
    #     self.assertEqual(fm.find_advertisement(find_iframe_web_driver, 'seprin.com'), None)
    #     self.assertEqual(fm.find_advertisement(find_iframe_web_driver, 'theworldnewsmedia.org'), None)
    #     # self.assertEqual(fm.find_advertisement(find_iframe_web_driver, 'canadianarchitect.com'), None)
    #     # self.assertEqual(fm.find_advertisement(find_iframe_web_driver, 'canadianconsultingengineer.com'), None)


if __name__ == '__main__':
    unittest.main()
