
from django.utils import timezone
from clicknetapp.models import iptable
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=5)
def delete_ip():
        for record in iptable.objects.all():
                exp = record.created_date + timedelta(minutes=1)
                if exp <= timezone.now():
                        record.delete()
        register_events(scheduler)