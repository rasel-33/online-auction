from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from accounts.models import GenderTypeChoices, UserTypeChoices, Profile

class RegisterUserForm(forms.ModelForm):
    repassword = forms.CharField( max_length=200, required=True)
    user_type = forms.ChoiceField(choices=UserTypeChoices.choices)
    gender = forms.ChoiceField(choices=GenderTypeChoices.choices)
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email', 'user_type', 'gender', 'password', 'repassword']

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['repassword']:
            self._errors["password"] = ["Password do not match"] # Will raise a error message
            del form_data['password']
        if User.objects.filter(username=form_data['username']).exists():
            self._errors['username'] = ["Username already exists"] #will raise an error message
        return form_data

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    class Meta:
        model=Profile
        fields=['first_name', 'last_name', 'user_image', 'phone', 'location']

class SignInForm(forms.ModelForm):
    username = forms.CharField(max_length=200,required=True)
    password = forms.PasswordInput()

    class Meta:
        model=User
        fields=['username', 'password']
        widgets = {
            'password':forms.PasswordInput(),
        }
