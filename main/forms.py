
from django import forms
class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class add_achievement(forms.Form):
    title=forms.CharField(required=True)
