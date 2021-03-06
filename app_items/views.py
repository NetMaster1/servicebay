from django.shortcuts import render, redirect
from .models import Item, Registry, RegistryLine, RegistryPending, RegistryLinePending, RegistryShopHold, RegistryLineShopHold, RegistryExpiring, RegistryLineExpiring, Status_change
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
            elif option == 'pending':
                return redirect('pending')
            elif option == 'expiring':
                return redirect('expiring')
            elif option == 'shop_hold':
                return redirect('shop_hold')
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
            warranty = request.POST.get('warranty', False)
            if warranty:
                cheque = request.POST.get('cheque', False)
                if cheque:
                    item = Item.objects.create(
                         shop=shop, user=user, brand=brand, model=model, imei=imei, comment=comment, full_set=full_set, client=client, status=status, phone=phone, defect=defect, date_of_purchase=date_of_purchase, warranty=True, cheque=True
                    )
                    # item.save()
                    status_change_date = Status_change.objects.create(
                        date_of_change=item.status_updated, status=item.status, imei=item.imei, brand=item.brand, model=item.model)
                    # status_change_date.save()
                    return render(request, 'order_used.html')
                else:
                    messages.error(request, ('Убедитесь в наличии чека'))
                    # return redirect('item')
                    return render (request, 'form.html')
           
            else:
                messages.error(request, ('Убедитесь в наличии гарантийного талона или узнайте в офисе об электронной гарантии'))
                return redirect('item')
            # try:
            #     if request.POST['warranty']:
            #         warranty = True
            # except KeyError:
            #     warranty = False      
        else:
            return render(request, 'form.html')
    else:
        return render(request, 'login.html')


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


def log(request):
    if request.user.is_authenticated:
        queryset = Item.objects.order_by('created')

        paginator = Paginator(queryset, 17)
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
    if request.user.is_authenticated:
        if request.method == "POST":
            item = Item.objects.get(id=item_id)
            item.status = request.POST['status']
            item.save()
            status_change_date = Status_change.objects.create(
                date_of_change=item.status_updated,
                status=item.status,
                imei=item.imei,
                brand=item.brand,
                model=item.model)
            status_change_date.save()
            queryset=Status_change.objects.filter(imei=item.imei)
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
                queryset_list = queryset_list.filter(status_updated=status_update_date)

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
        queryset = Item.objects.all()
    # date = datetime.datetime.now().date
    # date = datetime.datetime.now().year
        date = datetime.date.today()
        registry_pending = RegistryPending.objects.create()
        registry_pending.save()

        for item in queryset:
            if item.created==item.status_updated:
                timedelta = date - item.created
                td = timedelta.total_seconds()
                if td > 1209600:
                    RegistryLinePending.objects.create(
                        registry_pending=registry_pending,
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
                    item.save()
        queryset_list = RegistryLinePending.objects.filter(registry_pending=registry_pending.id)
        context = {
            'queryset_list': queryset_list,
            'date': date,
        }
        return render(request, 'pending.html', context)
    else:
        return redirect ('login')


def shop_hold(request):
    if request.user.is_authenticated:
        queryset = Item.objects.all()
    # date = datetime.datetime.now().date
    # date = datetime.datetime.now().year
        date = datetime.date.today()
        registry_shop_hold = RegistryShopHold.objects.create()
        # registry_expiring.save()

        for item in queryset:
            if item.status == 'Отправлен в СМТЕЛ' or item.status=='Отправлен на Горького' or item.status=='Отправлен в другой сервис. центр':
                timedelta = date - item.status_updated
                td = timedelta.total_seconds()
                if td > 2592000:
                    RegistryLineShopHold.objects.create(
                        registry_shop_hold=registry_shop_hold,
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
                    # item.save()
        queryset_list = RegistryLineShopHold.objects.filter(
            registry_shop_hold=registry_shop_hold.id)

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
    # date = datetime.datetime.now().date
    # date = datetime.datetime.now().year
        date = datetime.date.today()
        registry_expiring = RegistryExpiring.objects.create()
        # registry_expiring.save()

        for item in queryset:
                timedelta = date - item.created
                td = timedelta.total_seconds()
                if td > 2592000:
                    RegistryLineExpiring.objects.create(
                        registry_expiring=registry_expiring,
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
                    # item.save()
        queryset_list = RegistryLineExpiring.objects.filter(
            registry_expiring=registry_expiring.id)

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
