from django import forms

from vax.models import Parent

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name']
# class ParentForm(forms.Form):
#     first_name = forms.CharField(initial='first_name', required=True)
#     last_name = forms.CharField(initial='last_name', required=True)
