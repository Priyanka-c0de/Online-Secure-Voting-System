from django import forms

class QRRegisterForm(forms.Form):
    qr_data = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
