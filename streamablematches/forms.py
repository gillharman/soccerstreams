from django import forms

class AceStreamForm(forms.Form):
    ace_stream = forms.CharField(label="acestream://", max_length=100)