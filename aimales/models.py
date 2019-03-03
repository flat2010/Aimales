# Create your models here.
# -*- coding:utf8 -*-
from django.db import models
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField

class HttpRequest(models.Model):
    # 对应的数据包是否还有效
    is_valid = models.BooleanField(default=1)
    # 数据包名
    pcap_name = models.CharField(max_length=255, blank=True, null=True)
    # pcap的md5值
    pcap_md5 = models.CharField(max_length=255, blank=True, null=True)
    # pcap包存放的路径
    pcap_path = models.FileField(upload_to="datasets/http_request")
    # 相关样本总数(每个pcap有多个HTTP请求，每一个请求为一个样本)
    correlation_record_count = models.IntegerField(blank=True, null=True)
    # 负载内容(ascii)
    payload_ascii = models.TextField(blank=True, null=True)
    # 负载内容(binary)
    payload_binary = models.BinaryField(blank=True, null=True)
    # 负载大小(单个样本，字节)
    payload_size = models.IntegerField(blank=True, null=True)
    # 是否已标注
    is_tagged = models.BooleanField(default=0)
    # 标注结果
    word_tag_text = models.TextField(blank=True, null=True)
    # 标注结果数量
    word_tag_count = models.IntegerField(blank=True, null=True)
    # 是否已分词
    is_segmented = models.BooleanField(default=0)
    # 分词结果
    word_segmentation_text = models.TextField(blank=True, null=True)
    # 分词结果数量
    word_segmentation_count = models.IntegerField(blank=True, null=True)
    # 数据流捕获日期
    captured_date = models.DateTimeField(blank=True, null=True)
    # 创建日期
    add_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    # 最后更新日期
    update_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    # 上一次分词日期
    last_segmentation_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    # 上一次标注日期
    last_tag_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    # 备注信息
    remarks = models.TextField(blank=True, null=True)
    
    # 解决model_to_dict不显示日期字段问题
    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)

            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue

            if isinstance(f, ManyToManyField):
                value = [ i.id for i in value ] if self.pk else None

            if isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None

            data[f.name] = value

        return data
    
    def __unicode__(self):
        return self.content