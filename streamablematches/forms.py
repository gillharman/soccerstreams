from django import forms

class AceStreamForm(forms.Form):
    ace_stream = forms.CharField(widget=forms.TextInput(
        attrs={
            "autocomplete": "off",
            "placeholder": "acestream://",
            "size": 52
        }),
        label="Content ID",
        label_suffix="",
    )