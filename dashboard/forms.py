from django import forms
from django.forms import widgets
from . models import *

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields =['title','description']
class DateInput(forms.DateInput):
    input_type='date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields =['subject','title','description','due','is_finished']