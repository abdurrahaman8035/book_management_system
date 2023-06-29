from datetime import date, datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
    TemplateView,
    DetailView,
)
from django.urls import reverse_lazy, reverse
from .models import Student, Staff, StaffBook, StudentBook


class HomePageView(LoginRequiredMixin, TemplateView):
    """Display the HomePage"""

    template_name = "index.html"
    login_url = 'login'

    def get_context_data(self):
        total_books = StudentBook.objects.count() + StaffBook.objects.count()
        total_students = Student.objects.count()
        total_staff = Staff.objects.count()
        student_expired_books = StudentBook.objects.filter(expiring_date__lt=date.today())
        staff_expired_books = StaffBook.objects.filter(expiring_date__lt=date.today())
        total_expired_books = student_expired_books.count() + staff_expired_books.count()
        context = {
            "total_books": total_books,
            "total_students": total_students,
            "total_expired_books": total_expired_books,
            "total_staff": total_staff,
        }
        return context


class AddStudentBook(LoginRequiredMixin, CreateView):
    """Lend a Book to a Student"""

    model = StudentBook
    template_name = "addBook.html"
    fields = ['title']

    def get_success_url(self):
        pk = self.request.session.get('pk', None)
        # pk = self.object.id
        if pk:
            pk = pk
            # Clear the session
            self.request.session.flush()
        else:
            pk = None
        # pk = self.kwargs['pk']
        return reverse_lazy("books:profile", kwargs={"pk": pk})


class AddStaffBook(LoginRequiredMixin, CreateView):
    """Lend a Book to a staff"""

    model = StaffBook
    template_name = "addStaffBook.html"

    def get_success_url(self):
        staff = self.object.borrowed_by.id
        return reverse_lazy("books:staff_profile", kwargs={"staff_id": staff})


class StudentDetailView(LoginRequiredMixin, DetailView):
    """Display Student information and all books borrowed by the Student"""

    model = Student
    template_name = "student_profile.html"
    context_object_name = 'student'

    def get_queryset(self, **kwargs):
        context = super().get_queryset(**kwargs)
        pk = self.kwargs['pk']
        # Set the student ID on the session
        self.request.session['pk'] = pk
        # get all books borrowed by this student using related_name
        student = Student.objects.get(id=pk)

        for book in student.books.all():
            # calculate their remaining days left to expire
            book_expiring_date = datetime.date(book.expiring_date)
            current_date = date.today()

            time_left = (
                date(
                    book_expiring_date.year,
                    book_expiring_date.month,
                    book_expiring_date.day,
                )
            ) - current_date

            remaining_days = time_left.days

            result = str(remaining_days) + " day(s) remaining"
            # check if book has expired
            if remaining_days <= 0:
                # Calculate overdue charges: N20.00 per day. (-1) was used to get rid of negative values
                book.overdue = (remaining_days * (-1)) * 20
            book.remaining_days = result
            book.save()
        return context


class StaffDetailView(LoginRequiredMixin, DetailView):
    """Display a staff information and all books borrowed by the staff"""

    model = Staff
    template_name = "staff_profile.html"
    login_url = "login"

    def get_queryset(self, **kwargs):
        context = super().get_queryset(**kwargs)
        staff = self.get_object()
        # get all books borrowed by this student using related_name
        all_books = staff.books.all()

        for book in all_books:
            # calculate their remaining days left to expire
            book_expiring_date = datetime.date(book.expiring_date)
            current_date = date.today()

            time_left = (
                date(
                    book_expiring_date.year,
                    book_expiring_date.month,
                    book_expiring_date.day,
                )
            ) - current_date

            remaining_days = time_left.days

            result = str(remaining_days) + " day(s) remaining"
            # check if book has expired
            if remaining_days <= 0:
                # Calculate overdue charges: N20.00 per day. (-1) was used to get rid of negative values
                book.overdue = (remaining_days * (-1)) * 20
            book.remaining_days = result
            book.save()
        books = all_books
        context["books"] = books
        context["staff"] = staff
        return context


class all_studentsView(LoginRequiredMixin, ListView):
    """Display list of all Students registered"""
    model = Student
    template_name = "students_list.html"
    context_object_name = "students"
    total_students_count = Student.objects.count()
    extra_context = {"total_students_count": total_students_count}
    login_url = "login"


class StudentBookDelete(LoginRequiredMixin, DeleteView):
    """Remove a Student Book record"""
    model = StudentBook
    template_name = "student_book_delete.html"
    login_url = "login"
    pk_url_kwarg = 'pk'

    # get the student id from the url
    def get_success_url(self):
        student = self.kwargs['pk']
        return reverse_lazy("books:profile", kwargs={"pk": student})


class StaffBookDelete(LoginRequiredMixin, DeleteView):
    """Remove a Staff Book record"""
    model = StaffBook
    template_name = "deletestaffbook.html"
    context_object_name = "book"
    login_url = "login"

    # get the staff id from the url
    def get_success_url(self):
        staff_id = self.object.borrowed_by.pk
        return reverse_lazy("books:staff_profile", kwargs={"staff_id": staff_id})


class RenewStudentBookView(LoginRequiredMixin, UpdateView):
    """Renew a book borrowed by a student"""

    model = StudentBook
    fields = ["expiring_date"]
    template_name = "renewbook.html"
    context_object_name = "book"
    login_url = "login"

    # get the student id from the url
    def get_success_url(self):
        student = self.object.borrowed_by.pk
        return reverse_lazy("books:profile", kwargs={"pk": student})


class RenewStaffBookView(LoginRequiredMixin, UpdateView):
    """Renew a book borrowed by a staff"""

    model = StaffBook
    fields = ["expiring_date"]
    template_name = "renewstaffbook.html"
    context_object_name = "book"
    login_url = "login"

    # get the staff id from the url
    def get_success_url(self):
        staff = self.object.borrowed_by.pk
        return reverse_lazy("books:staff_profile", kwargs={"pk": staff})


class UserSearch(LoginRequiredMixin, ListView):
    """Display a search result for a particular student or staff"""

    model = Student
    login_url = "login"

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        student_list = Student.objects.filter(pk__icontains=query)
        if student_list:
            self.template_name = "student_search_result.html"
            total_result = student_list.count()
            self.extra_context = {"total_result": total_result}
            return student_list
        else:
            staff_list = Staff.objects.filter(staff_id__icontains=query)
            self.template_name = "staff_search_result.html"
            total_result = staff_list.count()
            self.extra_context = {"total_result": total_result}
            return staff_list


class RegisterStudent(LoginRequiredMixin, CreateView):
    """Add a new Student"""
    model = Student
    template_name = "register_student.html"
    fields = [
        "image",
        "first_name",
        "second_name",
        "pk",
        "Email",
        "phone_number",
        "year_of_admission",
        "level",
    ]
    login_url = "login"


class RegisterStaff(LoginRequiredMixin, CreateView):
    """Add a new Staff"""
    model = Staff
    template_name = "register_staff.html"
    fields = "__all__"
    login_url = "login"


class StudentEditProfile(UpdateView):
    """Edit a Student's information"""
    model = Student
    template_name = "student_edit_profile.html"
    fields = [
        "image",
        "first_name",
        "second_name",
        "pk",
        "Email",
        "phone_number",
        "year_of_admission",
        "level",
    ]
    context_object_name = "student"


class StaffEditProfile(UpdateView):
    """Edit Staff information"""
    model = Staff
    template_name = "staff_edit_profile.html"
    fields = ["image", "first_name", "second_name", "staff_id", "Email", "phone_number"]
    context_object_name = "staff"


class ExpiredBooksView(LoginRequiredMixin, ListView):
    """Display a list of expired books"""

    model = StudentBook
    template_name = "expired_books.html"
    login_url = "login"

    def get_queryset(self):
        student_expired_books = StudentBook.objects.filter(
            expiring_date__lt=date.today()
        )
        staff_expired_books = StaffBook.objects.filter(expiring_date__lt=date.today())
        context = {
            "student_expired_books": student_expired_books,
            "staff_expired_books": staff_expired_books,
        }
        return context


class AllBooksView(LoginRequiredMixin, ListView):
    """Display a list of all books"""

    template_name = "all_books.html"
    login_url = "login"

    def get_queryset(self):
        student_books_list = StudentBook.objects.all()
        staff_books_list = StaffBook.objects.all()
        context = {
            "student_books_list": student_books_list,
            "staff_books_list": staff_books_list,
        }
        return context


class AllStaffView(LoginRequiredMixin, ListView):
    """Display a list of all academic staff that borrowed books"""

    model = Staff
    context_object_name = "staff"
    template_name = "staff_list.html"
    login_url = "login"

    def get_queryset(self):
        staff_list = Staff.objects.all()
        return staff_list
