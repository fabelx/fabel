import sys
import os
import unittest

sys.path.append(os.getcwd())
import fabel

class TestDatabase(unittest.TestCase):
    # def test_insert_domain(self):
    #     db = fabel.DataBase('localhost', 'root', 'root01', 'fabel')
    #     connector_db = db.connect_to_db()
    #     self.assertEqual(db.insert_domain(connector_db, 8), 0)
    #     self.assertEqual(db.insert_domain(connector_db, 'gg'), 0)
    #     self.assertEqual(db.insert_domain(connector_db, 1), 0)
    #     self.assertEqual(db.insert_domain(connector_db, 2), 0)


    # def test_insert_into_db(self):
    #     db = fabel.DataBase('localhost', 'root', 'root01', 'fabel')
    #     connector_db = db.connect_to_db()
    #     self.assertEqual(db.insert_into_db(connector_db, 'googleads', 8, 'y'), 0)
    #     self.assertEqual(db.insert_into_db(connector_db, 'advertising', 1, 'y'), 0)

    def test_select_from_bd(self):
        db = fabel.DataBase('localhost', 'root', 'root01', 'fabel')
        self.assertEqual(db.select_from_db('*', "WHERE domain LIKE 'linuxfdfhgrthdg-community.de'", 26), [])
        self.assertEqual(db.select_from_db('hh', "WHERE domain LIKE 'linuxfdfhgrthdg-community.de'", 26), None)
        # self.assertEqual(db.select_from_db('domain', "WHERE domain LIKE 'linux-community.de'", 26000000), 'linux-community.de')


if __name__ == '__main__':
    unittest.main()