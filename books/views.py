from django.contrib import messages
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
from django.shortcuts import redirect
from .models import Student, Staff, StaffBook, StudentBook
from django.utils import timezone
from utils.book_factory import BookFactory
from .forms import StaffBookForm, StudentBookForm


class HomePageView(LoginRequiredMixin, TemplateView):
    """Display the HomePage"""

    template_name = "index.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_books"] = StudentBook.objects.count() + StaffBook.objects.count()
        context["total_students"] = Student.objects.count()
        context["total_expired_books"] = (
            StudentBook.objects.filter(expiring_date__lt=timezone.now().date()).count()
            + StaffBook.objects.filter(expiring_date__lt=timezone.now().date()).count()
        )
        context["total_staff"] = Staff.objects.count()
        return context


class StudentDetailView(LoginRequiredMixin, DetailView):
    """Display Student information and all books borrowed by the Student"""

    model = Student
    template_name = "student_profile.html"
    context_object_name = "student"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("books")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        books = student.books.all()
        for book in books:
            book_expiring_date = book.expiring_date
            remaining_days = (
                date(
                    book_expiring_date.year,
                    book_expiring_date.month,
                    book_expiring_date.day,
                )
                - date.today()
            ).days
            book.remaining_days = remaining_days
            # check if book has expired
            if book.remaining_days <= 0:
                # Calculate overdue charges: N20.00 per day. (-1) was used to get rid of negative values
                book.overdue = (remaining_days * (-1)) * 20
        context["books"] = books
        form = StudentBookForm()
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        student_id = self.kwargs["pk"]
        book_form = StudentBookForm(request.POST)
        if book_form.is_valid():
            book_info = book_form.cleaned_data
            book = BookFactory.assign_book_to_student(student_id, book_info)
            if book:
                messages.add_message(
                    request, messages.INFO, "Book assigned successfully."
                )
                return redirect("books:profile", pk=student_id)
            else:
                messages.add_message(request, messages.INFO, "Book not assigned.")
                return redirect("books:profile", pk=student_id)
        else:
            # Handle the case when the form is not valid
            messages.add_message(request, messages.INFO, "Form is not valid.")
            return redirect("books:profile", pk=student_id)


class StaffDetailView(LoginRequiredMixin, DetailView):
    """Display a staff information and all books borrowed by the staff"""

    model = Staff
    template_name = "staff_profile.html"
    context_object_name = "staff"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("books")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.object
        books = staff.books.all()
        for book in books:
            book_expiring_date = book.expiring_date
            remaining_days = (
                date(
                    book_expiring_date.year,
                    book_expiring_date.month,
                    book_expiring_date.day,
                )
                - date.today()
            ).days
            book.remaining_days = remaining_days
            # check if book has expired
            if book.remaining_days <= 0:
                # Calculate overdue charges: N20.00 per day. (-1) was used to get rid of negative values
                book.overdue = (remaining_days * (-1)) * 20
        context["books"] = books
        form = StaffBookForm()
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        staff_id = self.kwargs["pk"]
        book_form = StaffBookForm(request.POST)
        if book_form.is_valid():
            book_info = book_form.cleaned_data
            book = BookFactory.assign_book_to_staff(staff_id, book_info)
            if book:
                messages.add_message(
                    request, messages.INFO, "Book assigned successfully."
                )
                return redirect("books:staff_profile", pk=staff_id)
            else:
                messages.add_message(request, messages.INFO, "Book not assigned.")
                return redirect("books:staff_profile", pk=staff_id)
        else:
            # Handle the case when the form is not valid
            messages.add_message(request, messages.INFO, "Form is not valid.")
            return redirect("books:staff_profile", pk=staff_id)


class AllStudentsView(LoginRequiredMixin, ListView):
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
    context_object_name = 'book'
    login_url = "login"
    pk_url_kwarg = "pk"

    # get the student id from the url
    def get_success_url(self):
        student = self.kwargs["student_id"]
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
        return reverse_lazy("books:staff_profile", kwargs={"pk": staff_id})


class RenewStudentBookView(LoginRequiredMixin, UpdateView):
    """Renew a book borrowed by a student"""

    model = StudentBook
    fields = ["expiring_date"]
    template_name = "renewbook.html"
    context_object_name = "book"
    login_url = "login"

    # get the student id from the url
    def get_success_url(self):
        student = self.object.borrowed_by.id
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
        staff = self.object.borrowed_by.id
        return reverse_lazy("books:staff_profile", kwargs={"pk": staff})


class UserSearch(LoginRequiredMixin, ListView):
    """Display a search result for a particular student or staff"""

    model = Student
    login_url = "login"

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        student_list = Student.objects.filter(id_number__icontains=query)
        if student_list:
            self.template_name = "student_search_result.html"
            total_result = student_list.count()
            self.extra_context = {"total_result": total_result}
            return student_list
        else:
            staff_list = Staff.objects.filter(id_number__icontains=query)
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
        "id_number",
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
    fields = [
        "image",
        "first_name",
        "second_name",
        "id_number",
        "Email",
        "phone_number",
    ]
    login_url = "login"


class StudentEditProfile(UpdateView):
    """Edit a Student's information"""

    model = Student
    template_name = "student_edit_profile.html"
    fields = [
        "image",
        "first_name",
        "second_name",
        "id_number",
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
    fields = [
        "image",
        "first_name",
        "second_name",
        "id_number",
        "Email",
        "phone_number",
    ]
    context_object_name = "staff"


class ExpiredBooksView(LoginRequiredMixin, TemplateView):
    """Display a list of expired books"""

    template_name = "expired_books.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_expired_books = StudentBook.objects.filter(
            expiring_date__lt=date.today()
        )
        staff_expired_books = StaffBook.objects.filter(expiring_date__lt=date.today())
        context["books"] = student_expired_books
        context["staff_books"] = staff_expired_books
        return context


class AllBooksView(LoginRequiredMixin, TemplateView):
    """Display a list of all books"""

    template_name = "all_books.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_books_list = StudentBook.objects.all()
        staff_books_list = StaffBook.objects.all()
        context["student_books_list"] = student_books_list
        context["staff_books_list"] = staff_books_list
        return context


class AllStaffView(LoginRequiredMixin, ListView):
    """Display a list of all academic staff that borrowed books"""

    model = Staff
    context_object_name = "staff"
    template_name = "staff_list.html"
    login_url = "login"
    context_object_name = "staffs"

    def get_queryset(self):
        staffs = Staff.objects.all()
        return staffs
