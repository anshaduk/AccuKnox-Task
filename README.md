Topic: Django Signals

Question 1: By default are django signals executed synchronously or asynchronously? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic. 

Answer 1: By default , Django signals are executed synchronously.means that ,when a signal is sent,all connected receivers,(functions or methods listening for that signal) are called immediately and the main process waits for these receivers to complete before continuing.

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

############################################################################

Question 2: Do django signals run in the same thread as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

Answer 2: Django signals run in the same thread as the caller, we can use the threading module to print the current thread identifier in both the signal sender and the receiver. This will help us confirm that both are executed within the same thread.

# models.py 
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
import threading

@receiver(post_save, sender=Student)
def signal_receiver(sender, instance, **kwargs):
    print(f"Signal received in thread: {threading.current_thread().name}")

# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signal_app'

    def ready(self):
        import signal_app.signals

# test_thread.py
from myapp.models import Student
import threading

def create_instance():
    print(f"Creating Student instance in thread: {threading.current_thread().name}")
    my_instance = Student.objects.create(name="Test")
    print("Instance created.")

if __name__ == '__main__':
    create_instance()

The example shows that Django signals execute in the same thread as the caller, as evidenced by the matching thread names in the output.

############################################################################

Question 3: By default do django signals run in the same database transaction as the caller? Please support your answer with a code snippet that conclusively proves your stance. The code does not need to be elegant and production ready, we just need to understand your logic.

Answer 3: Yes, The Django signals run in the same database transaction as the caller, we can use a simple code snippet that performs database operations in both the main function and the signal receiver, then triggers a rollback to observe the behavior.

# models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()


# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
from django.db import transaction

@receiver(post_save, sender=Student)
def my_signal_receiver(sender, instance, **kwargs):
    print("Signal received. Modifying instance in the receiver...")
    instance.name = "Modified by Signal"
    instance.save()

# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signal_app'

    def ready(self):
        import signal_app.signals


# test_transaction.py
from django.db import transaction
from myapp.models import Student

def create_instance():
    try:
        with transaction.atomic():
            print("Creating Student instance...")
            student_instance = Student.objects.create(name="Initial Name")
            print(f"Instance created with name: {student_instance.name}")

            raise Exception("Triggering rollback")

    except Exception as e:
        print(f"Exception occurred: {e}")
    
    instance = Student.objects.filter(name="Modified by Signal").first()
    if instance:
        print(f"Instance found with name after rollback: {instance.name}")
    else:
        print("No instance found with the modified name. Rollback confirmed.")

if __name__ == '__main__':
    create_instance()

The Django signals run in the same database transaction as the caller. The rollback of the transaction also undo the changes made by the signal receiver, demonstrating their synchronous and transactional nature by default.

############################################################################
Topic: Custom Classes in Python

Description: You are tasked with creating a Rectangle class with the following requirements:

An instance of the Rectangle class requires length:int and width:int to be initialized.
We can iterate over an instance of the Rectangle class 
When an instance of the Rectangle class is iterated over, we first get its length in the format: {'length': <VALUE_OF_LENGTH>} followed by the width {width: <VALUE_OF_WIDTH>}

Answer:

class Rectangle:
    def __init__(self,length:int,width:int):
        self.length = length
        self.width = width
    
    def __iter__(self):
        return iter([{'length':self.length},{'width':self.width}])
        
rect = Rectangle(length=10,width=5)

for i in rect:
    print(i)


  
