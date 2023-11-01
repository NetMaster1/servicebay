from django.shortcuts import render, redirect
#from .models import Item, Registry, RegistryLine, Status_change
from django.contrib.auth.models import User, Group
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages, auth
from django.views import View
#from .utils import render_to_pdf
from io import BytesIO
from django.http import HttpResponse
import datetime
from datetime import date
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
import nexmo
import os
from twilio.rest import Client
from django.forms.fields import DateField
import serial
import time
from app_items.models import Item, Registry, RegistryLine, Status_change

# Create your views here.


def workshop_reports (request):
    if request.user.is_authenticated:
        items=Item.objects.all()
        if request.method == "POST":
            pass
        else:
            return render (request, 'reports/workshop_reports.html')

    else:
        return redirect('login')
