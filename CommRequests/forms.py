from django import forms
from .models import Requests
from main.models import  User

class RequestForm(forms.ModelForm):
    recipient = forms.CharField(label='Recipient Username')
    deadline = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Requests
        fields = [
            'project_name',
            'domain_of_project',
            'urgency',
            'subject',
            'content',
            'note',
            'deadline',
            'recipient'
        ]
    def clean_recipient(self):
        username = self.cleaned_data['recipient']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Invalid recipient username.")
        return username

class AssignRequestForm(forms.Form):
    recipients = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the queryset to non-staff users
        self.fields['recipients'].queryset = User.objects.filter(is_staff=False)