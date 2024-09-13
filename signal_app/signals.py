from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
import time

def student_signal_receiver(sender,instance,**kwargs):
    print("Signal received...process starting...")
    time.sleep(10)
    print('Signal process completed')
