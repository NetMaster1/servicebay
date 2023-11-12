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
<<<<<<< HEAD
            pass
=======
            # start_date = request.POST["start_date"]
            # start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            # end_date = request.POST["end_date"]
            # end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            # end_date = end_date + timedelta(days=1)
            status = request.POST["status"]
            queryset=Item.objects.filter(status=status)

             #==========================Convert to Excel module=========================================
            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = (
                "attachment; filename=SaleRep_" + str(date) + ".xls"
            )

            # str(datetime.date.today())+'.xls'

            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet('Statuses')

            # sheet header in the first row
            row_num = 0
            font_style = xlwt.XFStyle()
            columns = ['Дата создания', "Дата изменения статуса", 'IMEI', 'Бранд', 'Модель', 'Статус']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num + 1, columns[col_num], font_style)

            # sheet body, remaining rows
            font_style = xlwt.XFStyle()

            row_num = 1
            for item in queryset:
                col_num = 1
                ws.write(row_num, col_num, str(item.created), font_style)
                col_num +=1
                ws.write(row_num, col_num, str(item.status_updated), font_style)
                col_num +=1
                ws.write(row_num, col_num, item.imei, font_style)
                col_num +=1
                ws.write(row_num, col_num, item.brand, font_style)
                col_num +=1
                ws.write(row_num, col_num, item.model, font_style)
                col_num +=1
                ws.write(row_num, col_num, item.status, font_style)
                row_num +=1

            wb.save(response)
            return response

>>>>>>> bcc12ac58cb9470d7ba02ea77311120f98ca632e
        else:
            return render (request, 'reports/workshop_reports.html')

    else:
        return redirect('login')
