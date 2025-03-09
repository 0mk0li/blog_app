from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput,
        help_text="Enter a strong password.Use A-Z, a-z, special cahracters like @ etc. and numbers."
    )
    password2 = forms.CharField(
        required=True,
        label="Confirm password",
        widget=forms.PasswordInput,
        help_text="Enter same passowrd as above"
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        return password2
