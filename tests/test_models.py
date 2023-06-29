from django.test import TestCase
from django.urls import reverse
from books.models import Student, Staff, StudentBook, StaffBook
from django.db.models.signals import post_save
from django.utils.timezone import now
from utils.book_factory import BookFactory


class StudentModelTest(TestCase):
    def test_get_absolute_url(self):
        student = Student.objects.create(
            first_name="John",
            second_name="Doe",
            Email="john.doe@example.com",
            phone_number="1234567890",
            registration_date=now(),
            id_number="123456",
            email_sent=False,
        )
        expected_url = reverse("books:profile", kwargs={"pk": student.pk})
        self.assertEqual(student.get_absolute_url(), expected_url)


class StaffModelTest(TestCase):
    def test_get_absolute_url(self):
        staff = Staff.objects.create(
            first_name="John",
            second_name="Doe",
            Email="john.doe@example.com",
            phone_number="1234567890",
            registration_date=now(),
            id_number="123456",
            email_sent=False,
        )
        expected_url = reverse("books:staff_profile", kwargs={"pk": staff.pk})
        self.assertEqual(staff.get_absolute_url(), expected_url)


class StudentBookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = Student.objects.create(
            first_name="John",
            second_name="Doe",
            Email="john.doe@example.com",
            phone_number="1234567890",
            id_number="123456",
        )
        cls.book = StudentBook.objects.create(
            title="Book Title", borrowed_by=cls.student
        )

    def test_get_absolute_url(self):
        expected_url = reverse("books:profile", kwargs={"pk": self.student.id})
        self.assertEqual(self.book.get_absolute_url(), expected_url)

    def test_assign_book_to_student(self):
        new_book = BookFactory.assign_book_to_student(
            self.student.id, {"title": "Another Amazing Book Title"}
        )
        self.assertEqual(new_book.title, "Another Amazing Book Title")


class StaffBookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = Staff.objects.create(
            first_name="John",
            second_name="Doe",
            Email="john.doe@example.com",
            phone_number="1234567890",
            id_number="12345",
        )
        cls.book = StaffBook.objects.create(title="Book Title", borrowed_by=cls.staff)

    def test_get_absolute_url(self):
        expected_url = reverse("books:staff_profile", kwargs={"pk": self.staff.pk})
        self.assertEqual(self.book.get_absolute_url(), expected_url)

    def test_assign_book_to_staff(self):
        new_book = BookFactory.assign_book_to_staff(
            self.staff.id, {"title": "Another Amazing Book Title"}
        )
        self.assertEqual(new_book.title, "Another Amazing Book Title")


class SignalTest(TestCase):
    def test_send_email_to_student(self):
        student = Student.objects.create(
            first_name="John",
            second_name="Doe",
            Email="john.doe@example.com",
            phone_number="1234567890",
        )
        post_save.send(sender=Student, instance=student)
        student.refresh_from_db()
        self.assertTrue(student.email_sent)

    def test_send_email_to_staff(self):
        staff = Staff.objects.create(
            first_name="Jane",
            second_name="Smith",
            Email="jane.smith@example.com",
            phone_number="9876543210",
        )
        post_save.send(sender=Staff, instance=staff)
        staff.refresh_from_db()
        self.assertTrue(staff.email_sent)
