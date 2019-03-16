from django import forms


class GetDataForm(forms.Form):
    tree_data = forms.CharField(required=True, widget=forms.Textarea)
