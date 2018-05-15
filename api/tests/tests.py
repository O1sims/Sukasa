# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pickle
import unittest

from analytics.utilities.CollectPropertyData import get_final_page_number, get_all_main_images


class TestingPropertyCollection(unittest.TestCase):

    def test_final_page_number(self):
        with open('/home/owen/Code/Kasa/analytics/data/test_page.pkl') as f:
            first_page = pickle.load(f)
        page_number = get_final_page_number(
                first_page_soup=first_page)
        self.assertEqual(page_number, 54)

    def test_get_all_main_images(self):
        with open('/home/owen/Code/Kasa/analytics/data/test_page.pkl') as f:
            page_soup = pickle.load(f)
        main_images = get_all_main_images(page_soup=page_soup)
        self.assertEqual(len(main_images), 10)
        self.assertTrue(isinstance(main_images, list))
        self.assertTrue(isinstance(main_images[0], str))

if __name__ == '__main__':
    unittest.main()
