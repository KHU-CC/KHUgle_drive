from django import forms
from KHUgle.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'file']

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows':10}),
            'file' : forms.ClearableFileInput(attrs={'multiple': False, 'null':True})
        }

        def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            self.fields['file'].required = False

class DeletePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows':10}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'comment',
        }
