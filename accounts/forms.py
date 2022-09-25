from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from accounts.models import GenderTypeChoices, UserTypeChoices, Profile


class RegisterUserForm(forms.ModelForm):

    user_type = forms.ChoiceField(choices=UserTypeChoices.choices)
    gender = forms.ChoiceField(choices=GenderTypeChoices.choices)
    phone = forms.CharField(max_length=30, required=True)
    location = forms.CharField()


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'user_type', 'gender', 'location',
                  'password']
        widgets = {
            'password': forms.PasswordInput(),
            'repassword': forms.PasswordInput()
        }

    def clean(self):
        form_data = self.cleaned_data
        # if form_data['password'] != form_data['repassword']:
        #     self._errors["password"] = ["Password do not match"]  # Will raise a error message
        #     del form_data['password']
        if User.objects.filter(username=form_data['username']).exists():
            self._errors['username'] = ["Username already exists"]  # will raise an error message
        if User.objects.filter(email__iexact=form_data['email']).exists():
            self._errors['username'] = ["Email already exists"]
        return form_data


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'user_image', 'phone', 'location']


class SignInForm(forms.ModelForm):
    username = forms.CharField(max_length=200, required=True)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class RequestCreditForm(forms.Form):
    amount = forms.IntegerField(required=True)


class RequestWithdraw(forms.Form):
    amount = forms.IntegerField(required=True)


class ResetPasswordRequestForm(forms.Form):
    email = forms.EmailField()


class ResetPasswordForm(forms.Form):
    password = forms.CharField()
    password_confirm = forms.CharField()

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
            'password_confirm': forms.PasswordInput()
        }

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password_confirm']:
            self._errors["password"] = ["Password do not match"]  # Will raise a error message
            del form_data['password']
        return form_data
