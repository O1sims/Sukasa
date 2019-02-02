from __future__ import unicode_literals

import pickle
import unittest

from analytics.utilities.CollectPropertyData import \
    get_final_page_number, \
    get_all_main_images, \
    parse_epc_rating, \
    get_price


class TestingPropertyCollection(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestingPropertyCollection, self).__init__(*args, **kwargs)
        with open('analytics/data/test_page.pkl') as f:
            self.property_page = pickle.load(f)

    def test_final_page_number(self):
        page_number = get_final_page_number(
                first_page_soup=self.property_page)
        self.assertEqual(page_number, 54)

    def test_get_all_main_images(self):
        main_images = get_all_main_images(page_soup=self.property_page)
        self.assertEqual(len(main_images), 10)
        self.assertTrue(isinstance(main_images, list))
        self.assertTrue(isinstance(main_images[0], str))

    def test_get_price_info(self):
        property_details = self.property_page.findAll("div", {"class": "propbox-details"})
        price_info = get_price(page_soup=property_details[0])
        ideal_price_info = {
            'price': 155000,
            'minPrice': None,
            'maxPrice': None,
            'offer': 'Offers over',
            'currency': 'pound'
        }
        self.assertDictEqual(
            d1=price_info,
            d2=ideal_price_info)

    def test_parse_epc_rating(self):
        epc_rating_string = 'B82/B84'
        epc_rating_list = epc_rating_string.split('/')
        parsed_epc = parse_epc_rating(
            epc_rating_list=epc_rating_list)
        self.assertEqual(parsed_epc['actual']['score'], 82)
        self.assertEqual(parsed_epc['potential']['band'], 'B')
        self.assertEqual(parsed_epc['potential']['score'], 84)


if __name__ == '__main__':
    unittest.main()
