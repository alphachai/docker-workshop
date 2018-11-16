import json
import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormView

from scorekeeper.forms import ScoreForm

import requests

logger = logging.getLogger()

class ScoreView(FormView):
    template_name = 'score.html'
    form_class = ScoreForm
    success_url = '/score/'
