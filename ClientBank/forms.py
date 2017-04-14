from django import forms
from ClientBank.models import Users, UserInformation, User

class UsersFrom(forms.ModelForm):
    email = forms.CharField(max_length=50, help_text='Введите имейл')
    login = forms.CharField(max_length=25)
    password = forms.CharField(max_length=75)

    class Meta:
        # Создаем связь между ModelForm и моделью
        model = Users
        fields = '__all__'

class UsersInformationFrom(forms.ModelForm):


    class Meta:
        # Создаем связь между ModelForm и моделью
        model = UserInformation
        fields = ('FullName','Address','Phone')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)