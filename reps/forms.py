from django import forms

class WhereForm(forms.Form):
    """form for where a user lives"""
    where = forms.CharField(required=True, label="Where do you live ?")