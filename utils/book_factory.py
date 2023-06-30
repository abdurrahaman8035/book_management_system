from books.models import Student, Staff, StudentBook, StaffBook


class BookFactory:
    """Create and assign books to Student or Staff"""
    @staticmethod
    def assign_book_to_student(student_id, book_info):
        try:
            student = Student.objects.get(id=student_id)
            student_book = StudentBook.objects.create(**book_info)
            student_book.borrowed_by = student
            student_book.save()
            return student_book
        except Student.DoesNotExist:
            return None

    @staticmethod
    def assign_book_to_staff(staff_id, book_info):
        try:
            staff = Staff.objects.get(id=staff_id)
            staff_book = StaffBook.objects.create(**book_info)
            staff_book.borrowed_by = staff
            staff_book.save()
            return staff_book
        except Staff.DoesNotExist:
            return None