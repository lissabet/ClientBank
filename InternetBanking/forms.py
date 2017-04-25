from django import forms
from django.forms import ModelChoiceField

from InternetBanking.models import Users, UserInformation, User, Products, ProductType, ProductStatus
from InternetBanking.models import Currency, PhoneOperation, MobileOperators
import datetime
import random

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

class ChoiseForProductType(forms.ModelChoiceField):
  def label_from_instance(self, obj):
    return obj.TypeName

class ChoiseForCurrency(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.CurrencyName

class ProductForm(forms.ModelForm):
    TypeId = ChoiseForProductType(queryset=ProductType.objects.all())
    Balance = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    ContractDate = forms.DateField(widget=forms.HiddenInput(), initial= datetime.date.today)
    CurrencyId = ChoiseForCurrency(queryset=Currency.objects.all())
    EndContractDate = forms.DateField(widget=forms.SelectDateWidget)


    class Meta:
        model = Products
        fields = ('TypeId','CurrencyId','EndContractDate')

class ChoiseForMobileOperator(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.Name

class ChoiseForProduct(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        res = ''.join(obj.TypeId.TypeName + ' №'+ obj.ContractNumber + ' ' + obj.CurrencyId.CurrencyName)
        return res

class PhoneOperationForm(forms.ModelForm):
    MobileOperatorId = ChoiseForMobileOperator(queryset=MobileOperators.objects.all())
    ProductId = ChoiseForProduct(queryset=Products.objects.all())

    def __init__(self, eventUser, *args, **kwargs):
        super(PhoneOperationForm, self).__init__(*args, **kwargs)
        self.fields['ProductId'].queryset = Products.objects.filter(AccountNumber=eventUser.id)

    class Meta:
        model = PhoneOperation
        fields = ('PhoneNumber', 'MobileOperatorId', 'Amount','ProductId')