from django import forms
from .models import WordsModel, MemoModel

class MemoForm(forms.ModelForm):
    class Meta:
        model = MemoModel
        fields = ['memo']
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 5, 'style': 'width: 100%; max-width: 750px;'}),
        }
        
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))