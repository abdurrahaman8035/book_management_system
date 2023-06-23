from django.urls import path
from scanner.views import (
    HomeView,
    AllStudentsView,
    new_student_book,
    StudentDetailView,
    StudentBookDelete,
    RenewStudentBookView,
    UserSearch,
    Register_student,
    StudentEditProfile,
    ExpiredBooksView,
    AllBooksView,
    AllStaffView,
    StaffDetailView,
    new_staff_book,
    StaffBookDelete,
    RenewStaffBookView,
    StaffEditProfile,
    Register_staff,
)

app_name = "scanner"

urlpatterns = [
    path("", HomeView, name="home"),
    path("all_staff/", AllStaffView.as_view(), name="all_staff"),
    path("all_books/", AllBooksView.as_view(), name="all_books"),
    path("expired_books/", ExpiredBooksView.as_view(), name="expired_books"),
    path("register/", Register_student.as_view(), name="register_student"),
    path("search/", UserSearch.as_view(), name="search_student"),
    path("students/", AllStudentsView.as_view(), name="allstudents"),
    path("students/<int:student_id>/", StudentDetailView, name="profile"),
    path("book/<int:student_id>/", new_student_book, name="book-new"),
    path(
        "students/<int:student_id>/<int:pk>/delete",
        StudentBookDelete.as_view(),
        name="deletebook",
    ),
    path(
        "students/<int:student_id>/<int:pk>/renew",
        RenewStudentBookView.as_view(),
        name="renew-book",
    ),
    path(
        "students/<int:pk>/edit",
        StudentEditProfile.as_view(),
        name="edit_student_profile",
    ),
    path("register_staff/", Register_staff.as_view(), name="register_staff"),
    path("staff/<int:staff_id>/", StaffDetailView, name="staffprofile"),
    path("staff_book/<int:staff_id>/", new_staff_book, name="new_staff_book"),
    path(
        "staff/<int:staff_id>/<int:pk>/delete",
        StaffBookDelete.as_view(),
        name="delete_staff_book",
    ),
    path(
        "staff/<int:staff_id>/<int:pk>/renew",
        RenewStaffBookView.as_view(),
        name="renew_staff_book",
    ),
    path("staff/<int:pk>/edit", StaffEditProfile.as_view(), name="edit_staff_profile"),
]
