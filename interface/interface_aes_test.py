# _*_ coding: utf-8 _*_
# @Time: 2022/12/15 12:34
# @Author: river
# @File: interface_aes_test.py
from Crypto.Cipher import AES
import base64
import requests
import unittest
import json


class AESTest(unittest.TestCase):
    def setUp(self):
        BS = 16
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        self.base_url = "http://192.168.1.201:8000/api/sec_get_guest_list/"
        self.app_key = 'W7v4D60fds2Cmk2U'

    def encryptBase64(self, src):
        return base64.urlsafe_b64decode(src)

    def encryptAES(self, src, key):
        # 生成AES密文
        iv = b"1172311105789011"
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cryptor.encrypt(self.pad(src))
        return self.encryptBase64(ciphertext)

    def test_aes_interface(self):
        # test aes interface
        payload = {'eid': '1', 'phone': '18011001100'}
        # 加密
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")

    def test_get_guest_list_request_error(self):
        # eid is null
        payload = {'eid': '', 'phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], "eid cannot be empty")

    def test_get_guest_list_eid_error(self):
        # eid result is null
        payload = {'eid': '901', 'phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], "query result is empty")

    def test_get_guest_list_eid_success(self):
        # eid query success
        payload = {'eid': '1', 'phone': ''}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")
        self.assertEqual(result['data'][0]['realname'], "alen")
        self.assertEqual(result['data'][0]['phone'], "18011001100")

    def test_get_guest_list_eid_phone_null(self):
        # eid,phone query is null
        payload = {'eid': '2', 'phone': '10000000000'}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], "query result is empty")

    def test_get_guest_list_eid_phone_success(self):
        # eid,phone requests success
        payload = {'eid': '1', 'phone': '18011001100'}
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={"data": encoded})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], "success")
        self.assertEqual(result['data'][0]['realname'], "alen")
        self.assertEqual(result['data'][0]['phone'], "18011001100")


if __name__ == '__main__':
    unittest.main()
