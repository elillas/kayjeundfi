from django import forms
from .models import HomepageSoftware, BlogAndReview

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class HomepageSoftwareForm(forms.ModelForm):
    class Meta:
        model = HomepageSoftware
        fields = '__all__'

class BlogAndReviewForm(forms.ModelForm):
    class Meta:
        model = BlogAndReview
        fields = '__all__'
