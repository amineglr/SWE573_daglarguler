from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Story
from .models import Comment

class StoryForm(forms.ModelForm):
    
    class Meta:
        model = Story
        fields = ['content']


class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        exclude=["story"]
        labels = {
             "username" : "Your Username",
             "content" : "Your Comment",
        }
           

        
