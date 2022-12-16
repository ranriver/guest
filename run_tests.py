# _*_ coding: utf-8 _*_
# @Time: 2022/12/13 19:07
# @Author: river
# @File: run_tests.py
import time, sys
import unittest

sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
from unittest import defaultTestLoader
from db_fixture import test_data

# 指定测试用例为当前文件夹下的 interface 目录
test_dir = './interface'
# testsuit = defaultTestLoader.discover(test_dir, pattern='*_test.py')
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')
if __name__ == "__main__":
    test_data.init_data()  # 初始化接口测试数据

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='发布会签到系统接口自动化测试',
                            description='运行环境：MySQL(PyMySQL), Requests, unittest ')
    # runner.run(testsuit, rerun=0, save_last_run=False)
    runner.run(discover)
    fp.close()
