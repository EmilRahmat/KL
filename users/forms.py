from django import forms
from django.contrib.auth.forms import AuthenticationForm

class PhoneLoginForm(AuthenticationForm):
    username = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'placeholder': '+79991234567'}))

    def clean_username(self):
        phone = self.cleaned_data.get('username')
        if not phone.startswith('+7'):
            raise forms.ValidationError("Введите номер в формате +7...")
        return phone

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(label="Номер телефона", max_length=20)

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.startswith('+7'):
            raise forms.ValidationError("Введите номер в формате +7...")
        return phone
    
class CodeVerificationForm(forms.Form):
    code = forms.CharField(max_length=4)
