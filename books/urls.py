from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from books.views import (
    HomePageView,
    all_studentsView,
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
    path("book/new/", AddStudentBook.as_view(), name="book-new"),
    path(
        "book/<int:pk>/<int:student_id>/delete/",
        StudentBookDelete.as_view(),
        name="student_book_delete",
    ),
    path(
        "book/<int:pk>/<int:student_id>/renew/",
        RenewStudentBookView.as_view(),
        name="renew_student_book",
    ),
    path("books/", AllBooksView.as_view(), name="all_books"),
    path("expired_books/", ExpiredBooksView.as_view(), name="expired_books"),
    path("student/<int:pk>/", StudentDetailView.as_view(), name="profile"),
    path(
        "student/<int:pk>/edit/",
        StudentEditProfile.as_view(),
        name="student_edit_profile",
    ),
    path("student/new/", RegisterStudent.as_view(), name="register_student"),
    path("students/", all_studentsView.as_view(), name="all_students"),
    path("staff/new/", RegisterStaff.as_view(), name="register_staff"),
    path("staff/<int:pk>/edit/", StaffEditProfile.as_view(), name="staff_edit_profile"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff_profile"),
    path("staffs/", AllStaffView.as_view(), name="all_staff"),
    path("staff/book/<int:staff_id>/", AddStaffBook.as_view(), name="new_staff_book"),
    path(
        "staff/book/<int:pk>/<int:staff_id>/delete/",
        StaffBookDelete.as_view(),
        name="staff_book_delete",
    ),
    path(
        "staff/book/<int:pk>/<int:staff_id>/renew/",
        RenewStaffBookView.as_view(),
        name="renew_staff_book",
    ),
    path("search/", UserSearch.as_view(), name="user_search"),
    path("", HomePageView.as_view(), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
