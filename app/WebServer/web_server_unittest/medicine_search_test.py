# -*- encoding: utf-8 -*-
import sys
from imp import reload

reload(sys)
import MedicineSearch
import warnings
import web_server
import flask
from flask import Flask
import unittest


class MedicineSearchTestCase(unittest.TestCase):
    def test_something(self):
        warnings.filterwarnings(action='ignore')
        medicine = ["tylenol", "케토톱", "비타민", "부루펜", "키미테", "아스피린", "파스", "보나링", "펜잘", "게보린", "이가탄", "둘코락스", "활명수",
                    "베나치오"]
        required_keys = ['itemName', 'entpName', 'itemImage', 'depositMethodQesitm', 'seQesitm', 'useMethodQesitm']

        for m in medicine:
            data_list = MedicineSearch.crawler(m)
            for data in data_list:
                for key in required_keys:
                    # If the received data doesn't contain the item.
                    self.assertIn(key, data)

                    # If the value exists, check if the length of the data exceeds zero.
                    if data[key] is not None:
                        self.assertTrue(len(data[key]) > 0)
        warnings.filterwarnings(action='default')


class MyTestCase(unittest.TestCase):
    def test_something(self):
        warnings.filterwarnings(action='ignore')
        app = Flask(web_server.__name__)
        app.config['TESTING'] = True

        # Main page testing
        with web_server.app.test_client() as c:
            result = c.get('/')
            self.assertEqual(type(result), flask.wrappers.Response)
            self.assertEqual(result._status, "200 OK")

        # Medicine_list.html testing
        with web_server.app.test_client() as c:
            test_medicine = ["타이레놀", "비타민", "밴드", "파스", "부루펜", "후시딘", "인사돌", "이가탄", "겔포스"]

            for medicine in test_medicine:
                result = c.post("/search/medicine", data=dict(medicine_name=medicine), follow_redirects=True)
                self.assertEquals(result.status_code, 200)
        warnings.filterwarnings(action='default')


if __name__ == '__main__':
    unittest.main()
