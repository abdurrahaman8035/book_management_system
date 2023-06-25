from django.urls import path
from books.views import (
    HomePageView,
    AllStudentsView,
    StudentDetailView,
    StudentBookDelete,
    RenewStudentBookView,
    UserSearch,
    AddStudentBook,
    StudentEditProfile,
    ExpiredBooksView,
    AllBooksView,
    AllStaffView,
    StaffDetailView,
    AddStaffBook,
    StaffBookDelete,
    RenewStaffBookView,
    StaffEditProfile,
    RegisterStaff,
    RegisterStudent,
)

app_name = "books"

urlpatterns = [
    path("", HomePageView, name="home"),
    path("all_staff/", AllStaffView.as_view(), name="all_staff"),
    path("all_books/", AllBooksView.as_view(), name="all_books"),
    path("expired_books/", ExpiredBooksView.as_view(), name="expired_books"),
    path("register/", RegisterStudent.as_view(), name="register_student"),
    path("search/", UserSearch.as_view(), name="search_student"),
    path("students/", AllStudentsView.as_view(), name="allstudents"),
    path("students/<int:student_id>/", StudentDetailView, name="profile"),
    path("book/<int:student_id>/", AddStudentBook, name="book-new"),
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
    path("register_staff/", RegisterStaff.as_view(), name="register_staff"),
    path("staff/<int:staff_id>/", StaffDetailView, name="staffprofile"),
    path("staff_book/<int:staff_id>/", AddStaffBook, name="new_staff_book"),
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
