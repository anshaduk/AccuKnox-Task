from signal_app.models import Student

if __name__ == '__main__':
    print("Creating student instance..")
    student_instance = Student.objects.create(name = "Test name",age=25)
    print("Created Instance")