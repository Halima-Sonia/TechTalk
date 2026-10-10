from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'title',
            'category',
            'content',
            'featured_image',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your post title'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            }),

            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Write your post here...'
            }),

            'featured_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }