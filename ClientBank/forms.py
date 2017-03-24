from django import forms
from ClientBank.models import Users, UserInformation

class UsersFrom(forms.ModelForm):
    email = forms.CharField(max_length=50, help_text='Введите имейл')
    login = forms.CharField(max_length=25)
    password = forms.CharField(max_length=75)

    class Meta:
        # Создаем связь между ModelForm и моделью
        model = Users
        fields = '__all__'

class UsersInformationFrom(forms.ModelForm):
    FullName = forms.CharField(max_length=75, help_text='Введите имя')
    Address = forms.CharField(max_length=250)
    Phone = forms.CharField(max_length=15)

    class Meta:
        # Создаем связь между ModelForm и моделью
        model = Users
        fields = ['FullName','Address','Phone']