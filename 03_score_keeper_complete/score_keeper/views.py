import json
import logging

from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

import requests

logger = logging.getLogger()

class Test(PermissionRequiredMixin, View):
    permission_required = 'my_role'
    raise_exception = False

    def get(self, request):
        return HttpResponse('test')
