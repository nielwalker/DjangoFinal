from lms.models import *
from django import forms

class CourseInfoForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = "__all__"
        # widgets = {'user': forms.HiddenInput(), 'slug': forms.HiddenInput()}

class CourseDetailsForm(forms.ModelForm):
    class Meta:
        model = CourseDetails
        fields = "__all__"