from django import forms
from InternetBanking.models import Users, UserInformation, User, Products, ProductType, FlatPay
from InternetBanking.models import Currency, PhoneOperation, MobileOperators, InternetPay, InternetProviders
import datetime

class UsersFrom(forms.ModelForm):
    email = forms.CharField(max_length=50, help_text='Введите имейл')
    login = forms.CharField(max_length=25)
    password = forms.CharField(max_length=75)

    class Meta:
        # Создаем связь между ModelForm и моделью
        model = Users
        fields = '__all__'

class UsersInformationFrom(forms.ModelForm):
    FullName = forms.CharField(label="ФИО")
    Address = forms.CharField(label="Адрес")
    Phone = forms.CharField(label="Номер телефона")
    class Meta:
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
    TypeId = ChoiseForProductType(queryset=ProductType.objects.all(),label="Тип продукта")
    Balance = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    ContractDate = forms.DateField(widget=forms.HiddenInput(), initial= datetime.date.today)
    CurrencyId = ChoiseForCurrency(queryset=Currency.objects.all(),label="Вылюта продукта")
    EndContractDate = forms.DateField(widget=forms.SelectDateWidget,label="Срок действия продукта")


    class Meta:
        model = Products
        fields = ('TypeId','CurrencyId','EndContractDate')

class ChoiseForOperator(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.Name

class ChoiseForProduct(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        res = ''.join(obj.TypeId.TypeName + ' №'+ obj.ContractNumber + ' ' + obj.CurrencyId.CurrencyName)
        return res

class PhoneOperationForm(forms.ModelForm):
    MobileOperatorId = ChoiseForOperator(queryset=MobileOperators.objects.all())
    ProductId = ChoiseForProduct(queryset=Products.objects.all())

    def __init__(self, eventUser, *args, **kwargs):
        super(PhoneOperationForm, self).__init__(*args, **kwargs)
        self.fields['ProductId'].queryset = Products.objects.filter(AccountNumber=eventUser.id)

    class Meta:
        model = PhoneOperation
        fields = ('PhoneNumber', 'MobileOperatorId', 'Amount','ProductId')


class InternetPayForm(forms.ModelForm):
    InternetProviderId = ChoiseForOperator(queryset=InternetProviders.objects.all())
    ProductId = ChoiseForProduct(queryset=Products.objects.all())

    def __init__(self, eventUser, *args, **kwargs):
        super(InternetPayForm, self).__init__(*args, **kwargs)
        self.fields['ProductId'].queryset = Products.objects.filter(AccountNumber=eventUser.id)

    class Meta:
        model = InternetPay
        fields = ('ContractNumber', 'InternetProviderId', 'Amount', 'ProductId')

class FlatPayForm(forms.ModelForm):
    ProductId = ChoiseForProduct(queryset=Products.objects.all())

    def __init__(self, eventUser, *args, **kwargs):
        super(FlatPayForm, self).__init__(*args, **kwargs)
        self.fields['ProductId'].queryset = Products.objects.filter(AccountNumber=eventUser.id)

    class Meta:
        model = FlatPay
        fields = ('AccountNumber', 'Amount', 'ProductId')


class KeyForm(forms.Form):
    Key = forms.CharField()
