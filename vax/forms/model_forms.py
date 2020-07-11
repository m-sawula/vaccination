from django import forms

from vax.models import Parent

class ParentCreateForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ['create_date']
