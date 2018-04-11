from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# so we can use our model to dictate our form
from .models import Cat, Toy


class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ('name', 'breed', 'description', 'age')

class ToyForm(forms.ModelForm):
    class Meta:
        model = Toy
        fields = ('name',)


class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

# see extra codealong
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,)
    last_name = forms.CharField(max_length=30, required=False,)
    email = forms.EmailField(max_length=254, help_text='email is required')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class UploadPicture(forms.Form):
    image = forms.FileField(required=True)



# before we started using our model we defined our form manually here
# class CatForm(forms.Form):
#     name = forms.CharField(label='Name', max_length=100)
#     breed = forms.CharField(label='Breed', max_length=100)
#     description = forms.CharField(label='Description', max_length=250)
#     age = forms.IntegerField(label='Age')
