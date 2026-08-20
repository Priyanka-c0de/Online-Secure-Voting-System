from django import forms


class QRRegisterForm(forms.Form):
    qr_data = forms.CharField(required=False, widget=forms.HiddenInput())
    aadhaar = forms.CharField(
        required=False, max_length=12, min_length=12, label="Aadhaar Number"
    )
    name = forms.CharField(required=False, max_length=100)
    dob = forms.CharField(required=False)
    house = forms.CharField(required=False, max_length=255)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        qr_data = cleaned_data.get("qr_data")
        aadhaar = cleaned_data.get("aadhaar")

        if not qr_data and not aadhaar:
            raise forms.ValidationError(
                "Please scan the QR code or enter your Aadhaar number."
            )

        if qr_data and aadhaar:
            raise forms.ValidationError(
                "Please use either QR or Aadhaar registration, not both."
            )

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
