from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib.auth.models import User, Group,Permission
from django.core.exceptions import ValidationError

class CustomUserChangeForm(UserChangeForm):
    # groups = forms.ModelMultipleChoiceField(
    #     queryset=Group.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'password']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']

class user_email_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Email','type':'email'}),
            }

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name','required':''}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name','required':''}),
            'email': forms.TextInput(attrs={'type':'email','class': 'form-control', 'placeholder': 'example@gmail.com','required':''}),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')

        if not first_name:
            raise ValidationError({'first_name': 'First Name is required'})
        if not last_name:
            raise ValidationError({'last_name': 'Last Name is required'})
        if not email:
            raise ValidationError({'email': 'Email is required'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('This email is already in use.')
        return email

class UserChangeForm(UserChangeForm):
    password = None 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': ''}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com', 'required': ''}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            user_qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
            if user_qs.exists():
                raise forms.ValidationError('This email is already in use.')
        return email