from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title','content', 'category','image')
        labels = {
            'title':'Title',
            'category':'Category',
            'content':'Content',
            'image':'Image (Optional)'
        }
        widgets = {
            'title': forms.Textarea(attrs={'class':'form-control','id':"exampleFormControlTextarea1", 'rows':"2",'placeholder':'Type Your Title Here'}),
            'content': forms.Textarea(attrs={'class':'form-control','id':"exampleFormControlTextarea1", 'rows':"20",'placeholder':'Type Your Text Here ...'}),
            'category': forms.TextInput(attrs={'class':'form-control','placeholder':'Type Your category Here ...'}),
            'image':forms.ClearableFileInput(attrs={'class':'form-control', 'type':'file', 'id':'formFile'})
        }

class SignUpForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username','email','password')
        labels = {
            'username':'',
            'password':'',
            'email':'',
        }

        widgets = {
            'username':forms.TextInput(attrs={
                'placeholder':'Type your username here',
                'class':'field',
            }),
            'email':forms.EmailInput(attrs={
                'placeholder':'example@email.com',
                'class':'field',
            }),
            'password':forms.PasswordInput(attrs={
                'placeholder':'Type your password here',
                'class':'field password',
            }),
        }

        help_texts = {
            'username':None,
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('comment',)
        labels = {
            'comment':''
        }
        widgets = {
            'comment': forms.Textarea(attrs={'class':'form-control','id':"exampleFormControlTextarea1", 'rows':"3", 'placeholder':'Type Your Comment Here...'})
        }