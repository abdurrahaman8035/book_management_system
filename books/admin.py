from django.contrib import admin
from .models import Student, StudentBook, Staff, StaffBook
# Register your models here.

admin.site.register(Student)
admin.site.register(StudentBook)
admin.site.register(Staff)
admin.site.register(StaffBook)
