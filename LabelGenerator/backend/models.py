# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class SpanInformation(models.Model):
    trace_start_timestamp = models.CharField(max_length=64)
    trace_id = models.CharField(max_length=64)
    span_id = models.CharField(max_length=64)
    parent_span_id = models.CharField(max_length=64)
    span_start_timestamp = models.CharField(max_length=64)
    duration = models.CharField(max_length=64)
    operation_name = models.CharField(max_length=150)
    service_name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.span_id


class TraceInformation(models.Model):
    trace_id = models.CharField(max_length=64)
    label = models.IntegerField(default=0)

    def __unicode__(self):
        return self.trace_id
