from django import forms
from django.core.mail import send_mail

from .models import Category, SiteConfiguration


class CategoryAdminForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('slug',)

    def clean_name(self):
        data = self.cleaned_data['name']
        if data.lower() == 'popular':
            raise forms.ValidationError('The category can not be named "popular"')
        return data


class ContactForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message', 'rows': 4}), required=False)

    honeyp0t = forms.CharField(required=False, widget=forms.TextInput(attrs={'autocomplete': 'off', 'tabindex': -1}))

    def clean(self):
        cleaned_data = super().clean()
        honeyp0t = cleaned_data.get('honeyp0t')
        if honeyp0t:
            raise forms.ValidationError('You are robot')

    def send_email(self):
        email_list = SiteConfiguration.get_solo().email_list
        default_list = ['django@woodsenseinteriors.com']

        if email_list is not None:
            emails = email_list.split() or default_list
        else:
            emails = default_list

        try:
            message = """
Name: {}
Email: {}
Message: {}            
""".format(self.cleaned_data['name'], self.cleaned_data['email'], self.cleaned_data['message'])
            send_mail('WoodSense Contact Form', message, 'site@woodsenseinteriors.com', emails)
        except Exception as e:
            print(str(e))
