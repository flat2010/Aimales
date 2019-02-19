# Create your models here.
# -*- coding:utf8 -*-
from django.db import models


class HttpRequest(models.Model):
    # 对应的数据包是否还有效
    is_valid = models.BooleanField(default=0)
    # 数据包名
    pcap_name = models.CharField(max_length=255, blank=True, null=True)
    # pcap包存放的路径
    pcap_path = models.FileField(upload_to="datasets/http_request")
    # 负载内容(ascii)
    payload_ascii = models.TextField(blank=True, null=True)
    # 负载内容(binary)
    payload_binary = models.TextField(blank=True, null=True)
    # 远程、前端登录账户及密码
    remoteUser = models.TextField(blank=True, null=True)
    remotePwd = models.TextField(blank=True, null=True)
    webUser = models.TextField(blank=True, null=True)
    webPwd = models.TextField(blank=True, null=True)
    # 后台是否已经启用免密登录
    loginWithoutPwd = models.BooleanField(default=0)
    deviceType = models.CharField(max_length=255, blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    # 备注信息
    remarks = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.content