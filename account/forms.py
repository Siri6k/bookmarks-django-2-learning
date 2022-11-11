from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    # class pour le login authentification
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label='Mot de passe',
                               widget=forms.PasswordInput)
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe',
                               widget=forms.PasswordInput)
    pasword2 = forms.CharField(label='Repeté le mot de passe',
                               widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Mot de passe ne correspond pas.')
        return cd['password2']
    
    
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')