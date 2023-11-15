from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import scheduled_dispatch

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(scheduled_dispatch, 'interval', minutes=10)
	scheduler.start()