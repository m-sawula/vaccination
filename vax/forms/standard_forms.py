from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from vax.models import Parent


# formularz logowania współpracuje z class LoginView(View) w standard_views.py
class LoginForm(forms.Form):
    username = forms.CharField(label="Login", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


# class ChildForm(forms.Form):
#     SEX = (
#         ("M", "male"),
#         ("F", "female")
#     )
#     name = forms.CharField(label="First name", required=False)
#     surname = forms.CharField(label="Last name", required=False)
#     sex = forms.ChoiceField(choices=SEX, widget=forms.Select)
#     # band_name = forms.CharField(label="Band name")
#     date_of_birth = forms.DateField(
#         label="Birth date",
#         required=False,
#         widget=forms.SelectDateWidget
#     )
