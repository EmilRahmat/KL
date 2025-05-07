from django import forms

class PhoneLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15)
    
class CodeVerificationForm(forms.Form):
    code = forms.CharField(max_length=4)
