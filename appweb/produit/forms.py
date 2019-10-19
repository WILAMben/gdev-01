# yourapp.forms.py
from django import forms

from .models import Produit


class JoinForm(forms.Form):  # or forms.ModelForm
    email = forms.EmailField()
    name = forms.CharField(max_length=120)

    #dir un controleud de donnes li yedekhlou f form ta3ek
    def clean_email(self):
        email=self.cleaned_data.get("email")
        if email == "anis@gmail.com":
            raise forms.ValidationError("hadi machi valid")
        return email



