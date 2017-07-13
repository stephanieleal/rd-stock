from django import forms

class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(
        required = True,
        label="",
        max_length = 30,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        required = True,
        label="",
        max_length = 30,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
    )
    username = forms.CharField(
        required = True,
        label="",
        max_length = 32,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    email = forms.CharField(
        required = True,
        label="",
        max_length = 32,
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    password = forms.CharField(
        required = True,
        label="",
        max_length = 32,
        widget = forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
