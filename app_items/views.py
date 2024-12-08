from django.shortcuts import render, redirect
from .models import Item, Registry, RegistryLine, Status_change
from django.contrib.auth.models import User, Group
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages, auth
from django.views import View
from .utils import render_to_pdf
from io import BytesIO
from django.http import HttpResponse
import datetime
from datetime import date
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
import nexmo
import os
#from twilio.rest import Client
from django.forms.fields import DateField
import serial
import time

# Create your views here.


def choice(request):
    if request.user.is_authenticated:
        # checking if 'choice' name is in request.GET from radiobuttons
        if 'choice' in request.GET:
            option = request.GET['choice']
            if option == 'form':
                return redirect('item')
            elif option == 'log':
                return redirect('log')
            elif option == 'reports':
                return redirect ('workshop_reports')
            elif option == 'pending':
                return redirect('pending')
            elif option == 'expiring':
                return redirect('expiring')
            elif option == 'shop_hold':
                return redirect('shop_hold')
            elif option == 'commercial':
                return redirect('commercial')
            else:
                return redirect('presale')
        else:
            return render(request, 'choice.html')
    else:
        return redirect('login')

def item(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            shop = request.POST['shop']
            user = request.user
            brand = request.POST['brand']
            model = request.POST['model']
            imei = request.POST['imei']
            comment = request.POST['comment']
            full_set = request.POST['full_set']
            client = request.POST['client']
            status = "Принят на точке"
            phone = request.POST['phone']
            defect = request.POST['defect']
            date_of_purchase = request.POST['date_of_purchase']

            #======================Counting Number of Days From date of purchase to today=============
            field = DateField()
            formatted_date = field.to_python(date_of_purchase)
            delta = datetime.date.today() - formatted_date
            
            # current_date=datetime.date.today()
            # date = datetime.datetime.strptime(date_of_purchase, "%Y-%m-%d")
            # delta=current_date-date
            if delta.days > 365:
                messages.error(request, "Гарантийный срок истек")
                return redirect("item")
            else:
                # try:
                #     if request.POST['warranty']:
                #         warranty = True
                # except KeyError:
                #     warranty = False
                warranty = request.POST.get('warranty', False)
                if warranty:
                    cheque = request.POST.get('cheque', False)
                    if cheque:
                        item = Item.objects.create(
                            shop=shop,
                            user=request.user,
                            brand=brand,
                            model=model,
                            imei=imei,
                            comment=comment,
                            full_set=full_set,
                            client=client,
                            status=status,
                            phone=phone,
                            defect=defect,
                            date_of_purchase=date_of_purchase,
                            warranty=True,
                            cheque=True,
                        )
                        status_change_date = Status_change.objects.create(
                            date_of_change=item.status_updated,
                            status=item.status,
                            imei=item.imei,
                            brand=item.brand,
                            model=item.model
                        )
                        return render(request, 'order_used.html')
                    else:
                        messages.error(request, ('Убедитесь в наличии чека'))
                        #return redirect('item')
                        return render(request, 'form.html')
                else:
                    messages.error(
                        request, 'Убедитесь в наличии гарантийного талона или узнайте в офисе об электронной гарантии')
                    return redirect('item')   
        else:
            return render(request, 'form.html')
    else:
        return redirect('login')

def presale(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            shop = request.POST['shop']
            user = request.user
            brand = request.POST['brand']
            model = request.POST['model']
            imei = request.POST['imei']
            status = "Предпродажный"
            defect = request.POST['defect']

            item = Item.objects.create(
                shop=shop, user=user, brand=brand, model=model, imei=imei, status=status, defect=defect,
            )
            # item.save()
            status_change_date = Status_change.objects.create(
                date_of_change=item.status_updated, status=item.status, imei=item.imei, brand=item.brand, model=item.model)
            return render(request, 'order_presale.html')
        else:
            return render(request, 'presale.html')
    else:
        return render(request, 'login.html')

def commercial(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            brand = request.POST['brand']
            model = request.POST['model']
            imei = request.POST['imei']
            status = "Коммерческий"
            defect = request.POST['defect']

            item = Item.objects.create(
                user=user, brand=brand, model=model, imei=imei, status=status, defect=defect,
            )
            # item.save()
            status_change_date = Status_change.objects.create(
                date_of_change=item.status_updated, status=item.status, imei=item.imei, brand=item.brand, model=item.model)
            return render(request, 'order_presale.html')
        else:
            return render(request, 'commercial.html')
    else:
        return render(request, 'login.html')

def log(request):
    if request.user.is_authenticated:
        queryset = Item.objects.order_by('-id')

        paginator = Paginator(queryset, 50)
        page_number = request.GET.get('page')
        queryset_list = paginator.get_page(page_number)

        context = {
            'queryset_list': queryset_list,
        }
        return render(request, 'log.html', context)
    else:
        return render(request, 'login.html')

def card(request, item_id):
    if request.user.is_authenticated:
        item = Item.objects.get(id=item_id)
        queryset = Status_change.objects.filter(imei=item.imei)
        context = {
            'item': item,
            'queryset': queryset
        }
        return render(request, 'card.html', context)
    else:
        return render(request, 'login.html')

def update(request, item_id):
    import requests
    import json
    if request.user.is_authenticated:
        item = Item.objects.get(id=item_id)
        if request.method == "POST":
            item.status = request.POST['status']
            item.save()
            status_change_date = Status_change.objects.create(
                date_of_change=item.status_updated,
                status=item.status,
                imei=item.imei,
                brand=item.brand,
                model=item.model)
            status_change_date.save()
            queryset = Status_change.objects.filter(imei=item.imei)
            if item.status == 'Отправлен на точку':
                if item.phone:
                    #=============================Arduino API==============================
                    #ArduinoData = serial.Serial('/dev/ttyACM0', 19200)
                    #ArduinoData = serial.Serial('/dev/ttyACM0 (Arduino Uno)', 19200)
                    #ArduinoData = serial.Serial('com4', 19200)

                    #time.sleep(2)
                    ##phone=item.phone
                    #message=f'You phone {item.brand} {item.model} IMEI {item.imei} is ready.'
                    #messageToArd=f'{phone}:{message}\r'

                    #try:
                        #ArduinoData.write(messageToArd.encode())#encodes string to bytes
                        #res = bytes(phone_number)
                        #ArduinoData.write(messageToArd.encode('ascii'))
                        #ArduinoData.close()
                        #ArduinoData.flush()
                        #messages.success(request, "Клиенту было отослано сообщение о завершении ремонта.")
                    #except:
                        #messages.error(request, "Ошибка серийного порта.")
                    #=============================Smsc API=======================
                #В сообщении нужно обязательно указать отправителя, иначе спам фильтр не пропустит его.
                    phone=item.phone
                    message=f'ООО Ритейл. Ваше телефон {item.brand} {item.model} IMEI {item.imei} готов и завтра будет доставлен на точку.'
                    base_url="https://smsc.ru/sys/send.php?login=NetMaster&psw=ylhio65v&phones={}&mes=OOO Ритейл. Ваш телефон готов."
                    #base_url="https://smsc.ru/sys/send.php?login=NetMaster&psw=ylhio65v&phones={}&mes={}"
                    url=base_url.format(phone, message)
                    api_request=requests.get(url)
                    

                    # ===========Twilo API==================
                    # account_sid = 'ACb9a5209252abd7219e19a812f8108acc'
                    # auth_token = '264094dd9b5cb2c4e5f1ca939d1cd4e0'
                    # client = Client(account_sid, auth_token)
                    # message = client.messages \
                    #     .create(
                    #         body=f"Ваш телефон {item.brand} {item.model} IMEI {item.imei} готов и завтра в течение дня будет доставлен на точку. Пожалуйста, заберите его.",
                    #         from_='+16624993114',
                    #         to=item.phone
                    #     )
                    # print(message.sid)
                    # messages.success(request, "Клиенту было отослано сообщение о завершении ремонта.")
                # ================================
                else:
                    messages.error(request, "Сообщение не было отослано. Проверьте баланс или тип заявки.")
                # =============Nexmo API===========
                # client = nexmo.Client(key='264369ff', secret='cCGl0q81eNJ7mbWc')
                # client.send_message({
                #     'from': 'Vonage APIs',
                #     'to': item.phone,
                #     'text': 'Your phone is ready. Please, pick it up',
                # })
                # ======================================
            context = {
                'item': item,
                'queryset': queryset
            }
            return render(request, 'card.html', context)
    else:
        return redirect('login')

def search(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            queryset_list = Item.objects.all()
            imei = request.POST['imei']
            shop = request.POST['shop']
            brand = request.POST['brand']
            user = request.POST['user']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            status_update_date = request.POST['status_update_date']
            status = request.POST['status']
            if imei:
                queryset_list = queryset_list.filter(imei__icontains=imei)
            if shop:
                queryset_list = queryset_list.filter(shop__icontains=shop)
            if brand:
                queryset_list = queryset_list.filter(brand__icontains=brand)
            if user:
                queryset_list = queryset_list.filter(user__icontains=user)
            # if Q(start_date) | Q(end_date):
            #     queryset_list = queryset_list.filter(created__range=(start_date, end_date))
            if start_date:
                queryset_list = queryset_list.filter(created__gte=start_date)
            if end_date:
                queryset_list = queryset_list.filter(created__lte=end_date)
            if status:
                queryset_list = queryset_list.filter(status__icontains=status)
            if status_update_date:
                queryset_list = queryset_list.filter(
                    status_updated=status_update_date)

            registry = Registry.objects.create()
            registry.save()

            for item in queryset_list:
                RegistryLine.objects.create(
                    registry=registry,
                    user=item.user,
                    shop=item.shop,
                    brand=item.brand,
                    model=item.model,
                    imei=item.imei,
                    date_of_purchase=item.date_of_purchase,
                    phone=item.phone,
                    defect=item.defect,
                    comment=item.comment,
                    status=item.status,
                    client=item.client
                )

        context = {
            'queryset_list': queryset_list,
        }
        return render(request, 'search.html', context)
    else:
        return render(request, 'login.html')

def pending(request):
    if request.user.is_authenticated:
        date = datetime.date.today()
        queryset = Item.objects.all()
        for item in queryset:
            # if item.created == item.status_updated:
            delta = date-item.created
            item.delta_pending = delta.days
            item.save()
        queryset_list = Item.objects.filter(
            status='Принят на точке', delta_pending__gte=14)

        context = {
            'queryset_list': queryset_list,
            'date': date,
        }
        return render(request, 'pending.html', context)
    else:
        return redirect('login')

def shop_hold(request):
    if request.user.is_authenticated:
        date = datetime.date.today()
        queryset = Item.objects.all()
        for item in queryset:
            if item.status == 'Отправлен в СМТЕЛ' or item.status == 'Отправлен на Горького' or item.status == 'Отправлен в другой сервис. центр' or item.status == 'Отправлен в Галактику':
                delta = date - item.created
                item.delta_shop_hold = delta.days
                item.save()
        queryset_list = Item.objects.filter(
            status='Отправлен в СМТЕЛ', delta_shop_hold__gte=35)
        context = {
            'queryset_list': queryset_list,
            'date': date,
        }
        return render(request, 'shop_hold.html', context)
    else:
        return redirect('login')

def expiring(request):
    if request.user.is_authenticated:
        queryset = Item.objects.all()
        date = datetime.date.today()

        for item in queryset:
            delta = date - item.created
            item.delta_expiring = delta.days
            item.save()

        queryset_list = Item.objects.filter(delta_expiring__gte=37)

        context = {
            'queryset_list': queryset_list,
            'date': date,
        }
        return render(request, 'expiring.html', context)
    else:
        return redirect('login')

class DownloadPDF(View):
    # def get(self, request, *args, **kwargs):
    def get(self, request):
        order = Item.objects.latest('id')

        data = {
            'order': order,
        }
        pdf = render_to_pdf('pdf_order.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Order_%s.pdf" % (order.id)
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response

class DownloadPDF_log(View):
    # def get(self, request, *args, **kwargs):
    def get(self, request):
        registry = Registry.objects.latest('id')
        queryset_list = RegistryLine.objects.filter(registry=registry.id)
        data = {
            'queryset_list': queryset_list,
            'registry': registry
        }
        pdf = render_to_pdf('pdf_log.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Registry_%s.pdf" % (registry.id)
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response

class DownloadPDF_presale(View):
    # def get(self, request, *args, **kwargs):
    def get(self, request):
        order = Item.objects.latest('id')
        data = {
            'order': order,
        }
        pdf = render_to_pdf('pdf_presale.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Order_%s.pdf" % (order.id)
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
