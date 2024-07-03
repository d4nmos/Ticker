from django import forms

class BoardForm(forms.Form):
    text = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder': 'Введите текст'}))
    color = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'color', 'value': '#ffffff'}))