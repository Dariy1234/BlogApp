from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username:",
        max_length=155,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )

    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Username:",
        max_length=155,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )

    email = forms.EmailField(
        label="Email:",
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )

    password1 = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered!")

        return email

    def save(self, commit=True):
        user = super().save(commit)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        return user

