import importlib

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import (
    path,
    reverse_lazy,
)

from scorekeeper import views

app_name = 'scorekeeper'

urlpatterns = [
    path('', lambda x: HttpResponseRedirect(reverse_lazy('health_check_home'))),
    path('score/', views.ScoreView.as_view()),
]
