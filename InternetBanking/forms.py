from django import forms
from InternetBanking.models import Users, UserInformation, User, Products, ProductType, FlatPay
from InternetBanking.models import Currency, PhoneOperation, MobileOperators, InternetPay, InternetProviders
import datetime


class UsersInformationFrom(forms.ModelForm):
    FullName = forms.CharField(label="ФИО")
    Address = forms.CharField(label="Адрес")
    Phone = forms.CharField(label="Телефон")

    def __init__(self, *args, **kwargs):
        super(UsersInformationFrom, self).__init__(*args, **kwargs)
        self.fields['FullName'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['Address'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['Phone'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = UserInformation
        fields = ('FullName', 'Address', 'Phone')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Повторите пароль")
    username = forms.CharField(label="Логин")
    email = forms.CharField(label="Email")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['confirm_password'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control'
        })

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        if password1 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data

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
    TypeId = ChoiseForProductType(queryset=ProductType.objects.all(), label="Тип продукта", empty_label=None)
    Balance = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    ContractDate = forms.DateField(widget=forms.HiddenInput(), initial=datetime.date.today)
    CurrencyId = ChoiseForCurrency(queryset=Currency.objects.all(), label="Вылюта продукта", empty_label=None)
    EndContractDate = forms.DateField(widget=forms.SelectDateWidget, label="Срок действия продукта")

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['TypeId'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['CurrencyId'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['EndContractDate'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = Products
        fields = ('TypeId', 'CurrencyId', 'EndContractDate')




class ChoiseForOperator(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.Name


class ChoiseForProduct(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        res = ''.join(obj.TypeId.TypeName + ' №' + obj.ContractNumber + ' ' + obj.CurrencyId.CurrencyName)
        return res


class PhoneOperationForm(forms.ModelForm):
    MobileOperatorId = ChoiseForOperator(queryset=MobileOperators.objects.all(),label="Мобильный оператор",empty_label=None)
    ProductId = ChoiseForProduct(queryset=Products.objects.all(),label="Продукт ESBank", empty_label=None)
    PhoneNumber = forms.CharField(label="Номер телефона")
    Amount = forms.IntegerField(label="Сумма оплаты")

    def __init__(self, eventUser, *args, **kwargs):
        super(PhoneOperationForm, self).__init__(*args, **kwargs)
        self.fields['ProductId'].queryset = Products.objects.filter(AccountNumber=eventUser.id)
        self.fields['MobileOperatorId'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['ProductId'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['PhoneNumber'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['Amount'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = PhoneOperation
        fields = ('PhoneNumber', 'MobileOperatorId', 'Amount', 'ProductId')


class InternetPayForm(forms.ModelForm):
    InternetProviderId = ChoiseForOperator(queryset=InternetProviders.objects.all(), label="Провайдер",empty_label=None)
    ProductId = ChoiseForProduct(queryset=Products.objects.all(),label="Продукт ESBank", empty_label=None)
    ContractNumber = forms.CharField(label="Номер договора")
    Amount = forms.IntegerField(label="Сумма оплаты")

    def __init__(self, eventUser, *args, **kwargs):
        super(InternetPayForm, self).__init__(*args, **kwargs)
        self.fields['ProductId'].queryset = Products.objects.filter(AccountNumber=eventUser.id)
        self.fields['InternetProviderId'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['ProductId'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['ContractNumber'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['Amount'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = InternetPay
        fields = ('ContractNumber', 'InternetProviderId', 'Amount', 'ProductId')


class FlatPayForm(forms.ModelForm):
    ProductId = ChoiseForProduct(queryset=Products.objects.all(),label="Продукт ESBank", empty_label=None)
    AccountNumber = forms.CharField(label="Номер лицевого счета")
    Amount = forms.IntegerField(label="Сумма оплаты")

    def __init__(self, eventUser, *args, **kwargs):
        super(FlatPayForm, self).__init__(*args, **kwargs)
        self.fields['ProductId'].queryset = Products.objects.filter(AccountNumber=eventUser.id)
        self.fields['ProductId'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['AccountNumber'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['Amount'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = FlatPay
        fields = ('AccountNumber', 'Amount', 'ProductId')


class KeyForm(forms.Form):
    Key = forms.CharField(label="Ключ",widget=forms.PasswordInput())

    def __init__(self,  *args, **kwargs):
        super(KeyForm, self).__init__(*args, **kwargs)
        self.fields['Key'].widget.attrs.update({
            'class': 'form-control'
        })


class ChangePassword(forms.Form):
    email = forms.CharField(label="Введите email")

   


class RecoverCodeForm(forms.Form):
    code = forms.CharField(label="Код", required=False)


class NewPasswordForm(forms.Form):
    password = forms.CharField(label="Введите новый пароль", required=False, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Повторите пароль", required=False, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(NewPasswordForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        if password1 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data
