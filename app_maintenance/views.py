from django.shortcuts import render, redirect
from app_items.models import Item, Registry, RegistryLine, Status_change
from app_reference.models import Shop, Workshop, Brand, Status, Supplier

# Create your views here.

def update_all (request):
    if request.user.is_authenticated:
        items=Item.objects.all()
        shops=Shop.objects.all()
        workshops=Workshop.objects.all()
        brands=Brand.objects.all()
        statuses=Status.objects.all()
        suppliers=Supplier.objects.all()
        if request.method == "POST":
            #==================Statuses============================
            accepted=Status.objects.get(name='Принят на точке')
            presale=Status.objects.get(name='Предпродажный')
            to_be_sent_to_supplier=Status.objects.get(name='Ожидает отправки поставщику')
            sent_to_supplier=Status.objects.get(name='Отправлен поставщику')
            at_wshp_now=Status.objects.get(name='Отправлен на ремонт')
            at_commercial_rep_now=Status.objects.get(name='Отправлен в коммерческий ремонт')
            received_from_supplier=Status.objects.get(name='Получен обратно от поставщика')
            irreparability_doc=Status.objects.get(name='Получен Акт НРП')
            reimbursed=Status.objects.get(name='Получена компенсация')
            sent_back_to_shop=Status.objects.get(name='Отправлен на точку')
            client_reimbursed=Status.objects.get(name='Сделан возврат')
            moved_to_repair_shop=Status.objects.get(name='Перемещен на склад Ремонт')
            signed_off=Status.objects.get(name='Списан')
            #===================Suppliers=======================
            iton=Supplier.objects.get(name="АйтиОпт")
            other=Supplier.objects.get(name="Другой")
            rtk=Supplier.objects.get(name="РТК")
            sanavi=Supplier.objects.get(name="Санави")
            vvp=Supplier.objects.get(name="Центр дистрибьюции")
            smtel=Workshop.objects.get(name='СМТЕЛ')
            galaxy=Workshop.objects.get(name='Галактика')
            gorky_place=Workshop.objects.get(name='Мастерская на Горького')
            other_wshp=Workshop.objects.get(name='Другой')
            #===============Brands========================
            alcatel=Brand.objects.get(name='Alcatel')
            bq=Brand.objects.get(name='BQ')
            honor=Brand.objects.get(name='Honor')
            huawei=Brand.objects.get(name='Huawei')
            inoi=Brand.objects.get(name='Inoi')
            itel=Brand.objects.get(name='Itel')
            jinga=Brand.objects.get(name='Jinga')
            nokia=Brand.objects.get(name='Nokia')
            nokia=Brand.objects.get(name='Nokia')


            for item in items:
                if item.status == 'Принят на точке':
                    item.status_modified = accepted
                elif item.status == 'Предпродажный':
                    item.status_modified = presale
                elif item.status == 'Ожидает отправки в АйтиОпт':
                    item.status_modified = to_be_sent_to_supplier
                    item.supplier=iton
                elif item.status == 'Отправлен в Санави':
                    item.status_modified = sent_to_supplier
                    item.supplier=sanavi
                elif item.status == 'Отправлен в АйтиОпт':
                    item.status_modified = at_wshp_now
                    item.supplier=iton
                elif item.status == 'Отправлен в ЦД':
                    item.status_modified = sent_to_supplier
                    item.supplier=vvp
                elif item.status == 'Отправлен в РТК':
                    item.status_modified = sent_to_supplier
                    item.supplier=rtk
                elif item.status == 'Отправлен другому поставщику':
                    item.status_modified = sent_to_supplier
                    item.supplier=other
                elif item.status == 'Отправлен в СМТЕЛ':
                    item.status_modified = at_wshp_now
                    item.workshop=smtel
                elif item.status == 'Отправлен в Галактику':
                    item.status_modified = at_wshp_now
                    item.workshop=galaxy
                elif item.status == 'Отправлен в другой сервис. центр':
                    item.status_modified = at_wshp_now
                    item.workshop=other_wshp
                elif item.status == 'Отправлен в коммерческий ремонт':
                    item.status_modified = at_commercial_rep_now
                    item.workshop=smtel
                elif item.status == 'Получен обратно от поставщика':
                    item.status_modified = received_from_supplier
                elif item.status == 'Получен Акт НРП':
                    item.status_modified = irreparability_doc
                elif item.status == 'Получена компенсация':
                    item.status_modified = reimbursed
                elif item.status == 'Сделан возврат':
                    item.status_modified = client_reimbursed
                elif item.status == 'Списан':
                    item.status_modified = signed_off
                elif item.status == 'Перемещен на склад Ремонт':
                    item.status_modified = moved_to_repair_shop
                elif item.status == 'Отправлен на точку':
                    item.status_modified = sent_back_to_shop

                for brand in brands:
                    if item.brand==brand.name:
                        item.brand_modified=brand.name
                for shop in shops:
                    if item.shop==shop.name:
                        item.shop_modified=shop.name
                item.save()

            return redirect ('log')
        else:
            context = {

            }

    else:
        return redirect('login')