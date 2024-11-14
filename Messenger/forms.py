from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import User_Info

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email is already taken
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email


class User_InfoForm(forms.ModelForm):
    class Meta:
        model = User_Info
        fields = ['avatar', 'friends']

    def clean_friends(self):
        """Custom validation to prevent self-friendship."""
        friends = self.cleaned_data.get('friends')
        if self.instance.user in friends.all():
            raise forms.ValidationError("You cannot add yourself as a friend.")
        return friends