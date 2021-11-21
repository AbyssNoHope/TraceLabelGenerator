import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# @require_http_methods(["POST"])
# def 