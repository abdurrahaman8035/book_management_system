# from datetime import date, datetime
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import (
#     ListView,
#     DeleteView,
#     UpdateView,
#     CreateView,
#     TemplateView,
#     DetailView,
# )
# from django.urls import reverse_lazy
# from .models import Student, Staff, StaffBook, StudentBook


# class HomePageView(LoginRequiredMixin, TemplateView):
#     """Display the HomePage"""

#     template_name = "books\\index.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         total_books = StudentBook.objects.count() + StaffBook.objects.count()
#         total_students = Student.objects.count()
#         total_staff = Staff.objects.count()
#         student_expired_books = Book.objects.filter(expiring_date__lt=date.today())
#         staff_expired_books = StaffBook.objects.filter(expiring_date__lt=date.today())
#         total_expired_books = student_expired_books.count() + staff_expired_books.count()
#         context = {
#             "total_books": total_books,
#             "total_students": total_students,
#             "total_expired_books": total_expired_books,
#             "total_staff": total_staff,
#         }
#         return context


# class AddStudentBook(LoginRequiredMixin, CreateView):
#     """Lend a Book to a Student"""

#     model = StudentBook
#     template_name = "books\\addBook.html"

#     def get_success_url(self):
#         book = self.object
#         student = book.borrowed_by.pk
#         return reverse_lazy("books:profile", kwargs={"student_id": student})


# class AddStaffBook(LoginRequiredMixin, CreateView):
#     """Lend a Book to a staff"""

#     model = StaffBook
#     template_name = "books\\addStaffBook.html"

#     def get_success_url(self):
#         staff = self.object.borrowed_by.pk
#         return reverse_lazy("books:staffprofile", kwargs={"staff_id": staff})


# class StudentDetailView(LoginRequiredMixin, DetailView):
#     """Display Student information and all books borrowed by the Student"""

#     model = Student
#     template_name = "books\\student_profile.html"

#     def get_queryset(self, **kwargs):
#         context = super().get_queryset(**kwargs)
#         student = self.object.id
#         # get all books borrowed by this student using related_name
#         all_books = student.books.all()

#         for book in all_books:
#             # calculate their remaining days left to expire
#             book_expiring_date = datetime.date(book.expiring_date)
#             current_date = date.today()

#             time_left = (
#                 date(
#                     book_expiring_date.year,
#                     book_expiring_date.month,
#                     book_expiring_date.day,
#                 )
#             ) - current_date

#             remaining_days = time_left.days

#             result = str(remaining_days) + " day(s) remaining"
#             # check if book has expired
#             if remaining_days <= 0:
#                 # Calculate overdue charges: N20.00 per day. (-1) was used to get rid of negative values
#                 book.overdue = (remaining_days * (-1)) * 20
#             book.remaining_days = result
#             book.save()
#         books = all_books
#         context["books"] = books
#         context["student"] = student
#         return context


# class StaffDetailView(LoginRequiredMixin, DetailView):
#     """Display a staff information and all books borrowed by the staff"""

#     model = Staff
#     template_name = "books\\staff_profile.html"
#     login_url = "login"

#     def get_queryset(self, **kwargs):
#         context = super().get_queryset(**kwargs)
#         staff = self.object.id
#         # get all books borrowed by this student using related_name
#         all_books = staff.books.all()

#         for book in all_books:
#             # calculate their remaining days left to expire
#             book_expiring_date = datetime.date(book.expiring_date)
#             current_date = date.today()

#             time_left = (
#                 date(
#                     book_expiring_date.year,
#                     book_expiring_date.month,
#                     book_expiring_date.day,
#                 )
#             ) - current_date

#             remaining_days = time_left.days

#             result = str(remaining_days) + " day(s) remaining"
#             # check if book has expired
#             if remaining_days <= 0:
#                 # Calculate overdue charges: N20.00 per day. (-1) was used to get rid of negative values
#                 book.overdue = (remaining_days * (-1)) * 20
#             book.remaining_days = result
#             book.save()
#         books = all_books
#         context["books"] = books
#         context["staff"] = staff
#         return context


# class AllStudentsView(LoginRequiredMixin, ListView):
#     """Display list of all Students registered"""
#     model = Student
#     template_name = "books\\students_list.html"
#     context_object_name = "students"
#     total_students_count = Student.objects.count()
#     extra_context = {"total_students_count": total_students_count}
#     login_url = "login"


# class StudentBookDelete(LoginRequiredMixin, DeleteView):
#     """Remove a Student Book record"""
#     model = StudentBook
#     template_name = "books\\deletebook.html"
#     login_url = "login"

#     # get the student id from the url
#     def get_success_url(self):
#         student = self.object.borrowed_by.pk
#         return reverse_lazy("books:profile", kwargs={"student_id": student})


# class StaffBookDelete(LoginRequiredMixin, DeleteView):
#     """Remove a Staff Book record"""
#     model = StaffBook
#     template_name = "books\\deletestaffbook.html"
#     context_object_name = "book"
#     login_url = "login"

#     # get the staff id from the url
#     def get_success_url(self):
#         staff_id = self.object.borrowed_by.pk
#         return reverse_lazy("books:staffprofile", kwargs={"staff_id": staff_id})


# class RenewStudentBookView(LoginRequiredMixin, UpdateView):
#     """Renew a book borrowed by a student"""

#     model = StudentBook
#     fields = ["expiring_date"]
#     template_name = "books\\renewbook.html"
#     context_object_name = "book"
#     login_url = "login"

#     # get the student id from the url
#     def get_success_url(self):
#         student = self.object.borrowed_by.pk
#         return reverse_lazy("books:profile", kwargs={"student_id": student})


# class RenewStaffBookView(LoginRequiredMixin, UpdateView):
#     """Renew a book borrowed by a staff"""

#     model = StaffBook
#     fields = ["expiring_date"]
#     template_name = "books\\renewstaffbook.html"
#     context_object_name = "book"
#     login_url = "login"

#     # get the staff id from the url
#     def get_success_url(self):
#         staff = self.object.borrowed_by.pk
#         return reverse_lazy("books:staffprofile", kwargs={"staff_id": staff})


# class UserSearch(LoginRequiredMixin, ListView):
#     """Display a search result for a particular student or staff"""

#     model = Student
#     login_url = "login"

#     def get_queryset(self):
#         query = self.request.GET.get("search_box")
#         student_list = Student.objects.filter(id_number__icontains=query)
#         if student_list:
#             self.template_name = "books\\student_search_result.html"
#             total_result = student_list.count()
#             self.extra_context = {"total_result": total_result}
#             return student_list
#         else:
#             staff_list = Staff.objects.filter(staff_id__icontains=query)
#             self.template_name = "books\\staff_search_result.html"
#             total_result = staff_list.count()
#             self.extra_context = {"total_result": total_result}
#             return staff_list


# class RegisterStudent(LoginRequiredMixin, CreateView):
#     """Add a new Student"""
#     model = Student
#     template_name = "books\\register_student.html"
#     fields = [
#         "image",
#         "first_name",
#         "second_name",
#         "id_number",
#         "Email",
#         "phone_number",
#         "year_of_admission",
#         "level",
#     ]
#     login_url = "login"


# class RegisterStaff(LoginRequiredMixin, CreateView):
#     """Add a new Staff"""
#     model = Staff
#     template_name = "books\\register_staff.html"
#     fields = "__all__"
#     login_url = "login"


# class StudentEditProfile(UpdateView):
#     """Edit a Student's information"""
#     model = Student
#     template_name = "books\\edit_student_profile.html"
#     fields = [
#         "image",
#         "first_name",
#         "second_name",
#         "id_number",
#         "Email",
#         "phone_number",
#         "year_of_admission",
#         "level",
#     ]
#     context_object_name = "student"


# class StaffEditProfile(UpdateView):
#     """Edit Staff information"""
#     model = Staff
#     template_name = "books\\edit_staff_profile.html"
#     fields = ["image", "first_name", "second_name", "staff_id", "Email", "phone_number"]
#     context_object_name = "staff"


# class ExpiredBooksView(LoginRequiredMixin, ListView):
#     """Display a list of expired books"""

#     model = StudentBook
#     template_name = "books\\expired_books.html"
#     login_url = "login"

#     def get_queryset(self):
#         context = super().get_context_data()
#         student_expired_books = StudentBook.objects.filter(
#             expiring_date__lt=date.today()
#         )
#         staff_expired_books = StaffBook.objects.filter(expiring_date__lt=date.today())
#         context = {
#             "student_expired_books": student_expired_books,
#             "staff_expired_books": staff_expired_books,
#         }
#         return context


# class AllBooksView(LoginRequiredMixin, ListView):
#     """Display a list of all books"""

#     template_name = "books\\all_books.html"
#     login_url = "login"

#     def get_queryset(self):
#         student_books_list = StudentBook.objects.all()
#         staff_books_list = StaffBook.objects.all()
#         context = {
#             "student_books_list": student_books_list,
#             "staff_books_list": staff_books_list,
#         }
#         return context


# class AllStaffView(LoginRequiredMixin, ListView):
#     """Display a list of all academic staff that borrowed books"""

#     model = Staff
#     context_object_name = "staff"
#     template_name = "books\\all_staff.html"
#     login_url = "login"

#     def get_queryset(self):
#         staff_list = Staff.objects.all()
#         return staff_list
