from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Max
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from main.models import ProductionJ

JOURNAL = ProductionJ
# MODEL = Clorinesaltsprod
# COMMENTMODEL = CommentsClorinesaltsprod
URL = 'clorinesaltsprod'
NAME = 'хлористые соли приготовление'


class HeadView(View):
    """ Представление, которое выводит заглавную страницу журнала """
    """ Стандартное """

    def get(self, request):
        note = JOURNAL.objects.all().filter(for_url=URL)
        return render(request, URL + '/head.html', {'note': note, 'URL': URL})

