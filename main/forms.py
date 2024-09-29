from django import forms
from .models import ArtWork, Comment

class ArtWorkForm(forms.ModelForm):
    class Meta:
        model = ArtWork
        fields = ['title', 'image', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Поле для комментария