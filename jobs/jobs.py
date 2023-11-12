from django.conf import settings
import requests
import json
import random

def scheduled_dispatch():
 #=============================Smsc API=======================
	#В сообщении нужно обязательно указать отправителя, иначе спам фильтр не пропустит его.
	#phone=item.phone
	phone=79200711112
	#message=f'ООО Ритейл. Телефон {item.brand} {item.model} IMEI {item.imei} готов и завтра будет доставлен на точку.'
	message='Ваш телефон готов'
	base_url="https://smsc.ru/sys/send.php?login=NetMaster&psw=ylhio65v&phones={}&mes=OOO Ритейл. Ваш телефон готов."
	#base_url="https://smsc.ru/sys/send.php?login=NetMaster&psw=ylhio65v&phones={}&mes={}"
	url=base_url.format(phone, message)
	api_request=requests.get(url)

