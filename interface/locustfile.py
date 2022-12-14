# _*_ coding: utf-8 _*_
# @Time: 2022/12/16 17:10
# @Author: river
# @File: locustfile.py
from locust import HttpUser, TaskSet, task


# 定义用户行为
class UserBehavior(TaskSet):
    @task
    def baidu_page(self):
        self.client.get("/")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 3000
    max_wait = 6000
