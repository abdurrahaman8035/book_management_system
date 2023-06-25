from django.contrib import admin
from .models import Student, StudentBook, Staff, StaffBook, YearOfAdmission
# Register your models here.

admin.site.register(Student)
admin.site.register(StudentBook)
admin.site.register(YearOfAdmission)
# admin.site.register(Edit_Overdue_Charges)
admin.site.register(Staff)
admin.site.register(StaffBook)
