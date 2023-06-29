from django.test import TestCase
from django.urls import reverse
from books.models import Student, Staff, StudentBook, StaffBook
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name="John",
            second_name="Doe",
            Email="john.doe@example.com",
            phone_number="1234567890",
            id_number="123456",
        )
        self.staff = Staff.objects.create(
            first_name="Jane",
            second_name="Smith",
            Email="jane.smith@example.com",
            phone_number="9876543210",
            id_number="123456",
        )
        self.student_book = StudentBook.objects.create(
            title="Book Title", borrowed_by=self.student
        )
        self.staff_book = StaffBook.objects.create(
            title="Book Title", borrowed_by=self.staff
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="test12345",
            is_superuser=True
        )

    def test_home_page_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.get(reverse("books:home"))
        self.assertEqual(response.status_code, 200)

    def test_student_detail_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.get(reverse("books:profile", args=[self.student.id]))
        self.assertEqual(response.status_code, 200)

    def test_staff_detail_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.get(reverse("books:staff_profile", args=[self.staff.id]))
        self.assertEqual(response.status_code, 200)

    def test_all_students_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.get(reverse("books:all_students"))
        self.assertEqual(response.status_code, 200)

    def test_student_book_delete_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.post(
            reverse("books:student_book_delete", args=[self.student_book.id, self.student.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_staff_book_delete_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.post(
            reverse("books:staff_book_delete", args=[self.staff_book.id, self.staff.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_renew_student_book_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.post(
            reverse("books:renew_student_book", args=[self.student_book.id, self.student.id]), data={}
        )
        self.assertEqual(response.status_code, 302)

    def test_renew_staff_book_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.post(
            reverse("books:renew_staff_book", args=[self.staff_book.id, self.staff.id]), data={}
        )
        self.assertEqual(response.status_code, 302)

    def test_user_search_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.get(reverse("books:user_search"), data={"query": "123456"})
        self.assertEqual(response.status_code, 200)

    def test_register_student_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.post(
            reverse("books:register_student"),
            data={"first_name": "New Student", "id_number": "654321"},
        )
        self.assertEqual(response.status_code, 200)

    def test_register_staff_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.post(
            reverse("books:register_staff"), data={"first_name": "New Staff", "id_number": "210987"}
        )
        self.assertEqual(response.status_code, 200)

    def test_student_edit_profile_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.post(
            reverse("books:student_edit_profile", args=[self.student.id]),
            data={"first_name": "Updated Name"},
        )
        self.assertEqual(response.status_code, 200)

    def test_staff_edit_profile_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.post(
            reverse("books:staff_edit_profile", args=[self.staff.id]),
            data={"name": "Updated Name"},
        )
        self.assertEqual(response.status_code, 200)

    def test_expired_books_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.get(reverse("books:expired_books"))
        self.assertEqual(response.status_code, 200)

    def test_all_books_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.get(reverse("books:all_books"))
        self.assertEqual(response.status_code, 200)

    def test_all_staff_view(self):
        self.client.login(username="testuser", password="test12345")
        response = self.client.get(reverse("books:all_staff"))
        self.assertEqual(response.status_code, 200)
