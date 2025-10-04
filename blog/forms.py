from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from blog.models import Category, Post, PostComments        


 
class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True )
    message = forms.CharField(label='Message', required=True)


class  RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100, required=True)

    email    = forms.CharField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
    password_confirm = forms.CharField(label='Confirm Password', max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("passwords do not match")   


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    titles = forms.CharField(label='Title', max_length=100, required=True)
    contents = forms.CharField(label='Content', max_length=1000, widget=forms.Textarea, required=True)
    category = forms.ModelChoiceField(
    label='Category',
    queryset=Category.objects.all(),
    required=True,
    empty_label='Select a category'
)
    image_urls = forms.ImageField(label='image', required=False)

    class Meta:
        model = Post
        fields = ['titles', 'contents', 'category', 'image_urls']
    def clean(self):
        cleaned_data =  super().clean()    
        titles = cleaned_data.get('titles')
        contents = cleaned_data.get('contents')

        if titles and len(titles) <5:
            raise forms.ValidationError('title must be more than 5 characters')
        if contents and len(contents) <10:
            raise forms.ValidationError('content must be more 10 characters')
        
class Comment_Post(forms.ModelForm):
    class Meta:
        model = PostComments
        fields = ['name', 'content', 'email']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

