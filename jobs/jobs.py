from django.conf import settings
from app_items.models import Item
import datetime
import time
import requests
import json
import random

def scheduled_dispatch():
	date = datetime.date.today()
	items=Item.objects.all()
	for item in items:
		delta = date - item.created
		item.delta_pending = delta.days
		item.save()
	items= Item.objects.filter(status='Принят на точке', delta_pending__gte=7)
		
 #=============================Smsc API=======================
	#В сообщении нужно обязательно указать отправителя, иначе спам фильтр не пропустит его.
	#phone=item.phone
	phone='79527644417'
	for item in items:
		message=f'ООО Ритейл. {item.brand} {item.model} IMEI {item.imei} 7 дн. в {item.shop}.'
		#print(message)
		#message='Ваш телефон готов'
		#base_url="https://smsc.ru/sys/send.php?login=NetMaster&psw=ylhio65v&phones={}&mes=OOO Ритейл. Ваш телефон готов."
		base_url="https://smsc.ru/sys/send.php?login=NetMaster&psw=ylhio65v&phones={}&mes={}"
		url=base_url.format(phone, message)
		api_request=requests.get(url)
		print(api_request.status_code)
		time.sleep(60)

