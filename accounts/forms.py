from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = Account
        fields = ('email', 'first_name', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-element'


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email2 = self.cleaned_data['email2']
        user.first_name = self.cleaned_data['first_name']   
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()

        return user


class AccountUpdateForm( forms.ModelForm ):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Account
        exclude = ('password','is_active', 'is_staff')
        fields = ('email', 'first_name', 'last_name', 'is_active', 'phone')

    
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-element'

    
    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.email = self.cleaned_data['email']
        account.first_name = self.cleaned_data['first_name']
        account.last_name = self.cleaned_data['last_name']
        account.phone = self.cleaned_data['phone']

        if commit:
            account.save()

        return account