from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address', required=True)


    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            ]


# Profile Form
class ProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
            ]


class SocialRegisterForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'email'
            ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
