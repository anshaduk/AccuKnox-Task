Topic: Django Signals

Question 1: By default are django signals executed synchronously or asynchronously? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic. 
Answer 1: By default , Django signals are executed synchronously.means ,when a signal is sent,all connected receivers,(functions or methods listening for that signal) are called immediately and the main process waits for these receivers to complete before continuing.

# models.py
from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
import time

def student_signal_receiver(sender,instance,**kwargs):
    print("Signal received...process starting...")
    time.sleep(10)
    print('Signal process completed')

# test_signals.py
from signal_app.models import Student

if __name__ == '__main__':
    print("Creating student instance..")
    student_instance = Student.objects.create(name = "Test name",age=25)
    print("Created Instance")
    
# __init__.py
default_app_config = 'signal_app.apps.SignalAppConfig'

So, i conclude that , The output confirms that the signal handling is synchronous because the program waits for the receiver function to finish (including the 10 second sleep) before proceeding to print "Created Instance" If the signals were asynchronous, "created Instance" would appear immediately without waiting for the signal processing to complete.


  
