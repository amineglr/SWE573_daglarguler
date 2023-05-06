from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Story

class StoryForm(forms.ModelForm):
    
    class Meta:
        model = Story
        fields = ['content']