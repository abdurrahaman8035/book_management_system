from django.test import TestCase
from django.urls import reverse
from books.models import Student, Staff, StudentBook, StaffBook
from django.db.models.signals import post_save


class StudentModelTest(TestCase):
    def test_get_absolute_url(self):
        student = Student.objects.create(
            first_name="John",
            second_name="Doe",
            Email="john.doe@example.com",
            phone_number="1234567890",
        )
        expected_url = reverse("books:profile", kwargs={"pk": student.id})
        self.assertEqual(student.get_absolute_url(), expected_url)


class StaffModelTest(TestCase):
    def test_get_absolute_url(self):
        staff = Staff.objects.create(
            first_name="Jane",
            second_name="Smith",
            Email="jane.smith@example.com",
            phone_number="9876543210",
        )
        expected_url = reverse("books:staff_profile", kwargs={"pk": staff.id})
        self.assertEqual(staff.get_absolute_url(), expected_url)


class StudentBookModelTest(TestCase):
    def test_get_absolute_url(self):
        student = Student.objects.create(
            first_name="John",
            second_name="Doe",
            Email="john.doe@example.com",
            phone_number="1234567890",
        )
        book = StudentBook.objects.create(title="Book Title", borrowed_by=student)
        expected_url = reverse("books:profile", kwargs={"pk": student.id})
        self.assertEqual(book.get_absolute_url(), expected_url)


class StaffBookModelTest(TestCase):
    def test_get_absolute_url(self):
        staff = Staff.objects.create(
            first_name="Jane",
            second_name="Smith",
            Email="jane.smith@example.com",
            phone_number="9876543210",
        )
        book = StaffBook.objects.create(title="Book Title", borrowed_by=staff)
        expected_url = reverse("books:staff_profile", kwargs={"pk": staff.pk})
        self.assertEqual(book.get_absolute_url(), expected_url)


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
