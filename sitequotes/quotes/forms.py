from django import forms
from .models import Quotes, Source


class AddQuoteForm(forms.ModelForm):
    class Meta:
        model = Quotes
        fields = ['text_quotes', 'weight', 'source']
        text_quotes = forms.CharField(widget=forms.Textarea())
        weight = forms.IntegerField(initial=1)
        source = forms.ModelChoiceField(queryset=Source.objects.all())

        labels = {
            'text_quotes': 'Цитата',
            'weight': 'Вес',
            'source': 'Источник',
        }
