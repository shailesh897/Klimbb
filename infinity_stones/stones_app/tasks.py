from celery import shared_task
from django.utils import timezone
from .models import Activation
import time

@shared_task
def process_stone_activation(activation_id):
    activation = Activation.objects.get(id=activation_id)
    activation.start_time = timezone.now()
    activation.save()
    
    time.sleep(activation.power_duration)
    
    activation.end_time = timezone.now()
    activation.save()
