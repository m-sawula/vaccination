from django import forms

from vax.models import Parent, Child, Vax


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name']


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'sex', 'date_of_birth']


class VaxForm(forms.ModelForm):
    class Meta:
        model = Vax
        fields = ['vax_date', 'symptom_after_vax']
