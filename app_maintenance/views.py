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
            at_smtel_now=Status.objects.get(name='Отправлен в СМТЕЛ')
            at_sanavi_now=Status.objects.get(name='Отправлен в Санави')
            at_galaktika_now=Status.objects.get(name='Отправлен в Галактику')
            at_gorky_now=Status.objects.get(name='Отправлен на Горького')
            at_other_wshp_now=Status.objects.get(name='Отправлен в другой сервис. центр')
            at_commercial_rep_now=Status.objects.get(name='Отправлен в коммерческий ремонт')
            sent_to_iton=Status.objects.get(name='Отправлен в АйтиОпт')
            sent_to_vvp=Status.objects.get(name='Отправлен в ЦД')
            sent_to_rtk=Status.objects.get(name='Отправлен в РТК')
            sent_to_other_supplier=Status.objects.get(name='Отправлен другому поставщику')
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


            for item in items:
                if item.status == 'Принят на точке':
                    item.status_modified = accepted
                elif item.status == 'Предпродажный':
                    item.status_modified = presale
                elif item.status == 'Ожидает отправки в АйтиОпт':
                    item.status_modified = to_be_sent_to_supplier
                    item.supplier=iton
                elif item.status == 'Отправлен в СМТЕЛ':
                    item.status_modified = at_smtel_now
                elif item.status == 'Отправлен в Санави':
                    item.status_modified = at_sanavi_now
            
                    pass
        else:
            context = {

            }

    else:
        return redirect('login')