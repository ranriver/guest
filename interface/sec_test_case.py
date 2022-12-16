# _*_ coding: utf-8 _*_
# @Time: 2022/12/15 11:43
# @Author: river
# @File: sec_test_case.py
import requests
import unittest


class GetEventListTest(unittest.TestCase):
    # 查询发布会信息（带用户认证）
    def setUp(self):
        self.base_url = "http://192.168.1.201:8000/api/sec_get_event_list"

    def test_get_event_list_auth_null(self):
        # auth为空
        r = requests.get(self.base_url, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 10011)
        self.assertEqual(result['message'], "user auth null")

    def test_get_event_list_auth_error(self):
        # auth错误
        auth_user = ('abc', '123')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 10012)
        self.assertEqual(result['message'], "user auth fail")

    def test_get_event_list_eid_null(self):
        # eid参数为空
        auth_user = ('admin', 'admin123456')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], "parameter error")

    def test_get_event_list_eid_success(self):
        # 根据eid查询结果成功
        auth_user = ('admin', 'admin123456')
        r = requests.get(self.base_url, auth=auth_user, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")


if __name__ == "__main__":
    unittest.main()
