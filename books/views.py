from django.shortcuts import render

# Create your views here.
# from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from .models import Book, Student, Staff, Staff_Book
from datetime import *
from django.urls import reverse_lazy
from .forms import *

# Create your views here.

# send_mail(subject='Greeting from librarian software',
#           recipient_list=['abdurrahamanabdullahi20@gmail.com'])


@login_required()
def HomeView(request):
    total_books = Book.objects.count() + Staff_Book.objects.count()
    total_students = Student.objects.count()
    total_staff = Staff.objects.count()
    student_expired_books = Book.objects.filter(expiring_date__lt=date.today())
    staff_expired_books = Staff_Book.objects.filter(expiring_date__lt=date.today())
    expired_books = len(student_expired_books) + len(staff_expired_books)
    context = {
        "total_books": total_books,
        "total_students": total_students,
        "expired_books": expired_books,
        "total_staff": total_staff,
    }
    return render(request, "scanner\\index.html", context)


@login_required()
def new_student_book(request, student_id):
    """Add a new book for a particular student."""
    student = Student.objects.get(id=student_id)
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = BookForm()
    else:
        # POST data submitted; process data.
        form = BookForm(data=request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.borrowed_by = student
            book.save()
            return redirect("scanner:profile", student_id=student_id)
    # Display a blank or invalid form.
    context = {"student": student, "form": form}
    return render(request, "scanner\\addBook.html", context)


@login_required()
def new_staff_book(request, staff_id):
    """ "Add a new book for a particular staff."""
    staff = Staff.objects.get(id=staff_id)
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = StaffBookForm()
    else:
        # POST data submitted; process data.
        form = StaffBookForm(data=request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.borrowed_by = staff
            book.save()
            return redirect("scanner:staffprofile", staff_id=staff_id)
    # Display a blank or invalid form.
    context = {"staff": staff, "form": form}
    return render(request, "scanner\\addStaffBook.html", context)


@login_required()
def StudentDetailView(request, student_id):
    """Show a single student and all books borrowed by students."""
    student = Student.objects.get(id=student_id)
    # get all books borrowed by this student
    all_books = student.books.all()

    for book in all_books:
        # calculate their remaining days left to expire
        b = datetime.date(book.expiring_date)

        time_left = (date(b.year, b.month, b.day)) - date.today()

        result = str(time_left.days) + " day(s) remaining"
        # check if book has expired
        if time_left.days < 0:
            book.overdue = (time_left.days * (-1)) * 20
        book.rem_days = result
        book.save()
    books = all_books
    context = {"books": books, "student": student}
    return render(request, "scanner\\student_profile.html", context)


@login_required()
def StaffDetailView(request, staff_id):
    """Show a single staff and all books borrowed by the staff."""
    staff = Staff.objects.get(id=staff_id)
    # get all books borrowed by this student
    all_books = staff.books.all()

    for book in all_books:
        # calculate their remaining days left to expire
        b = datetime.date(book.expiring_date)

        days_left = (date(b.year, b.month, b.day)) - date.today()

        result = str(days_left.days) + " day(s) remaining"
        # check if book has expired
        if days_left.days < 0:
            book.overdue = (days_left.days * (-1)) * 20
        book.rem_days = result
        book.save()
    books = all_books
    context = {"books": books, "staff": staff}
    return render(request, "scanner\\staff_profile.html", context)


class AllStudentsView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "scanner\\students_list.html"
    context_object_name = "students"
    total_students = Student.objects.count()
    extra_context = {"total_students": total_students}
    login_url = "login"


class StudentBookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "scanner\\deletebook.html"

    # get the student id from the url
    def get_success_url(self):
        student = self.object.borrowed_by.pk
        return reverse_lazy("scanner:profile", kwargs={"student_id": student})


class StaffBookDelete(LoginRequiredMixin, DeleteView):
    model = Staff_Book
    template_name = "scanner\\deletestaffbook.html"
    context_object_name = "book"

    # get the staff id from the url
    def get_success_url(self):
        staff_id = self.object.borrowed_by.pk
        return reverse_lazy("scanner:staffprofile", kwargs={"staff_id": staff_id})


class RenewStudentBookView(LoginRequiredMixin, UpdateView):
    """Renew a book borrowed by a student"""

    model = Book
    fields = ["expiring_date"]
    template_name = "scanner\\renewbook.html"
    context_object_name = "book"
    login_url = "login"

    # get the student id from the url
    def get_success_url(self):
        student = self.object.borrowed_by.pk
        return reverse_lazy("scanner:profile", kwargs={"student_id": student})


class RenewStaffBookView(LoginRequiredMixin, UpdateView):
    """Renew a book borrowed by a staff"""

    model = Staff_Book
    fields = ["expiring_date"]
    template_name = "scanner\\renewstaffbook.html"
    context_object_name = "book"
    login_url = "login"

    # get the staff id from the url
    def get_success_url(self):
        staff = self.object.borrowed_by.pk
        return reverse_lazy("scanner:staffprofile", kwargs={"staff_id": staff})


class UserSearch(LoginRequiredMixin, ListView):
    """Display a search result for a particular student or staff"""

    model = Student
    login_url = "login"

    def get_queryset(self):
        query = self.request.GET.get("search_box")
        object_list = Student.objects.filter(id_number__icontains=query)
        if object_list:
            self.template_name = "scanner\\student_search_result.html"
            total_result = len(object_list)
            self.extra_context = {"total_result": total_result}
            return object_list
        else:
            object_list = Staff.objects.filter(staff_id__icontains=query)
            self.template_name = "scanner\\staff_search_result.html"
            total_result = len(object_list)
            self.extra_context = {"total_result": total_result}
            return object_list


class Register_student(LoginRequiredMixin, CreateView):
    model = Student
    template_name = "scanner\\register_student.html"
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


class Register_staff(LoginRequiredMixin, CreateView):
    model = Staff
    template_name = "scanner\\register_staff.html"
    fields = "__all__"
    login_url = "login"


class StudentEditProfile(UpdateView):
    model = Student
    template_name = "scanner\\edit_student_profile.html"
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
    model = Staff
    template_name = "scanner\\edit_staff_profile.html"
    fields = ["image", "first_name", "second_name", "staff_id", "Email", "phone_number"]
    context_object_name = "staff"


class ExpiredBooksView(LoginRequiredMixin, ListView):
    """Display a list of expired books"""

    model = Book
    template_name = "scanner\\expired_books.html"
    login_url = "login"

    def get_queryset(self):
        books = Book.objects.filter(expiring_date__lt=date.today())
        staff_expired_books = Staff_Book.objects.filter(expiring_date__lt=date.today())
        self.extra_context = {"books": books, "staff_books": staff_expired_books}
        return books, staff_expired_books


class AllBooksView(LoginRequiredMixin, ListView):
    """Display a list of all books"""

    model = Book
    template_name = "scanner\\all_books.html"
    login_url = "login"

    def get_queryset(self):
        student_books = Book.objects.all()
        staff_books = Staff_Book.objects.all()
        self.extra_context = {"books": student_books, "staff_books": staff_books}
        return student_books, staff_books


class AllStaffView(LoginRequiredMixin, ListView):
    """Display a list of all academic staff that borrowed books"""

    model = Staff
    context_object_name = "staffs"
    template_name = "scanner\\all_staff.html"
    login_url = "login"

    def get_queryset(self):
        object_list = Staff.objects.all()
        return object_list
