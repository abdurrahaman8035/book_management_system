from django.forms.models import ModelForm
from .models import StudentBook, StaffBook


class StudentBookForm(ModelForm):
    """A simple form for collecting student books information"""

    class Meta:
        """Additional information for the Class"""
        model = StudentBook
        fields = ["title"]


class StaffBookForm(ModelForm):
    """A simple form for collecting staff books information"""

    class Meta:
        """Additional information for the Class"""
        model = StaffBook
        fields = ["title"]
