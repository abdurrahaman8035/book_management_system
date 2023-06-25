from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.urls import reverse
from django.core.mail import EmailMessage


LEVEL_CHOICES = [
    ("remedials", "Remedials"),
    ("100", "100 Level"),
    ("200", "200 Level"),
    ("300", "300 Level"),
    ("400", "400 Level"),
]


class YearOfAdmission(models.Model):
    """Year of entry for Students"""

    year = models.CharField(max_length=9)

    class Meta:
        """Additional information for the Class"""

        verbose_name_plural = "years of admission"

    def __str__(self):
        return f"{self.year}".title()


class UserAbstractModel(models.Model):
    """Abstract Class for Student and Staff Classes"""

    class Meta:
        """Additional infromation for the Class"""

        abstract = True

    image = models.ImageField(upload_to="images//%Y/%m/%d/", blank=False, null=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(null=True, blank=True, default=False)
    sms_sent = models.BooleanField(null=True, blank=True, default=False)


class Student(UserAbstractModel, models.Model):
    """Database table for students information"""

    class Meta:
        """Additional information for the Student Class"""

        ordering = ["-registration_date"]
        verbose_name_plural = "students"

    student_id = models.CharField(max_length=15, unique=True)
    year_of_admission = models.ForeignKey(
        YearOfAdmission, on_delete=models.CASCADE, null=True, blank=True
    )
    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
    )

    def get_absolute_url(self):
        """Return student profile URL"""
        return reverse("scanner:profile", kwargs={"student_id": self.pk})

    def __str__(self):
        return f"{self.first_name}".title() + " " + f"{self.second_name}".title()


class Staff(UserAbstractModel, models.Model):
    """Database table for staff information"""

    class Meta:
        """Additional information for the Staff Class"""

        ordering = ["-registration_date"]
        verbose_name_plural = "staff"

    staff_id = models.CharField(max_length=15, unique=True)

    def get_absolute_url(self):
        """Return staff profile URL"""
        return reverse("scanner:staffprofile", kwargs={"staff_id": self.pk})

    def __str__(self):
        return f"{self.first_name}".title() + " " + f"{self.second_name}".title()


class BookAbstractModel(models.Model):
    """Abstract Class for StudentBook and StaffBook Classes"""

    class Meta:
        """Additional information for the Class"""

        abstract = True

    title = models.CharField("Book title", max_length=100)
    issued_date = models.DateTimeField(default=datetime.now())
    added_days = models.IntegerField(null=True, blank=True)
    remaining_days = models.CharField(max_length=100, null=True, blank=True)
    expiring_date = models.DateTimeField(
        default=(datetime.today() + timedelta(days=14)), null=True, blank=True
    )


class StudentBook(BookAbstractModel, models.Model):
    """Create a book borrowed by a Student"""

    class Meta:
        """Additional information for the Class"""

        ordering = ["-issued_date"]

    borrowed_by = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="books", null=True, blank=True
    )

    def get_absolute_url(self):
        """Return Student Profile URL"""
        student_id = self.borrowed_by.pk
        return reverse("scanner:profile", kwargs={"student_id": student_id})

    def __str__(self):
        return self.title[:50]


class StaffBook(BookAbstractModel, models.Model):
    """Create a book borrowed by a Staff"""

    class Meta:
        """Additional information for the Class"""
        ordering = ["-issued_date"]

    borrowed_by = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="books", null=True, blank=True
    )

    def get_absolute_url(self):
        """Return a Staff Profile URL"""
        staff_id = self.borrowed_by.pk
        return reverse("scanner:staffprofile", kwargs={"staff_id": staff_id})

    def __str__(self):
        return self.title[:50]


@receiver(post_save, sender=Student, dispatch_uid="send_email_to_student")
def send_email_to_student(**kwargs):
    """Send Email to newly registered Student after successful registration"""
    student = kwargs["instance"]
    student_name = str(student.first_name) + " " + str(student.second_name)
    student_email = student.Email
    message = (
        f"Dear {student_name}, thanks for registering with us! Attached is our rules"
        " and regulations for you to read! Thank you so much."
    )
    # Check if email not sent
    if not student.email_sent:
        # Resend the email
        email_subject = "Registration Successful!"
        email = EmailMessage(email_subject, message, [student_email])
        # Attach the Library Rules and Regulations document to the Email
        email.attach_file("static/files/rules_and_regulations.pdf")
        email.send(fail_silently=False)
        student.email_sent = True
        print("sending email...")
        print(message)
        student.save()


@receiver(post_save, sender=Staff, dispatch_uid="send_email_to_staff")
def send_email_to_staff(**kwargs):
    """Send Email to newly registered Staff after sucessful registration"""
    staff = kwargs["instance"]
    staff_name = str(staff.first_name) + " " + str(staff.second_name)
    staff_email = staff.Email
    message = (
        f"Dear {staff_name}, thanks for registering with us! Attached is our rules"
        " and regulations for you to read! Thank you so much."
    )
    # Check if email not sent
    if not staff.email_sent:
        # Resend the email
        email_subject = "Registration Successful!"
        email = EmailMessage(email_subject, message, [staff_email])
        # Attach the Library Rules and Regulations document to the Email
        email.attach_file("static/files/rules_and_regulations.pdf")
        email.send(fail_silently=False)
        staff.email_sent = True
        print("sending email...")
        print(message)
        staff.save()


class OverDueCharges(models.Model):
    """Charges for late returning of Books"""

    overdue = models.IntegerField()

    class Meta:
        """Additional information for the Class"""

        verbose_name_plural = "overdue charges"

    def __str__(self):
        value = self.overdue
        return "The current overdue charges is " + str(value) + " naira per day"
