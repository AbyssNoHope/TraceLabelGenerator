# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class TraceInformation(models.Model):
    trace_uuid = models.CharField(max_length=64)
    trace_start_timestamp = models.BigIntegerField()
    label = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)

    def __unicode__(self):
        return self.trace_uuid


class SpanInformation(models.Model):
    trace = models.ForeignKey(
        to=TraceInformation, on_delete=models.CASCADE, null=True)
    span_uuid = models.CharField(max_length=64)
    parent_span_uuid = models.CharField(max_length=64)
    span_start_timestamp = models.BigIntegerField()
    duration = models.BigIntegerField()
    operation_name = models.CharField(max_length=150)
    service_name = models.CharField(max_length=64)
    error_message = models.CharField(max_length=64, blank=True, default='')

    def __unicode__(self):
        return self.span_uuid
