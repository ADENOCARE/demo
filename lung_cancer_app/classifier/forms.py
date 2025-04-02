from django import forms
from .models import Story

class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['name', 'role', 'story']