import datetime
from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    email = models.CharField(max_length=50)
    login = models.CharField(max_length=25)
    password = models.CharField(max_length=75)

class Roles(models.Model):
    name = models.CharField(max_length=50)

class UserInformation(models.Model):
    UserId = models.ForeignKey(User)
    FullName = models.CharField(max_length=75)
    Address = models.CharField(max_length=250)
    Phone = models.CharField(max_length=50)
    RoleId = models.ForeignKey(Roles)


class ProductStatus(models.Model):
    StatusName = models.CharField(max_length=20)


class ProductType(models.Model):
    TypeName = models.CharField(max_length=50)


class Currency(models.Model):
    CurrencyName = models.CharField(max_length=100)
    CurrencyCode = models.CharField(max_length=5)


class Products(models.Model):
    TypeId = models.ForeignKey(ProductType)
    Balance = models.IntegerField(default=0)
    AccountNumber = models.ForeignKey(User)
    ContractNumber = models.CharField(max_length=10)
    ContractDate = models.DateField(default=datetime.date.today)
    EndContractDate = models.DateField()
    StatusId = models.ForeignKey(ProductStatus)
    CurrencyId = models.ForeignKey(Currency)


class Operations(models.Model):
    OperationName = models.CharField(max_length=70)
    OperationCost = models.IntegerField()


class UserOperations(models.Model):
    UserId = models.ForeignKey(Users)
    OperationId = models.ForeignKey(Operations)


class MobileOperators(models.Model):
    Name = models.CharField(max_length=15)


class PhoneOperation(models.Model):
    UserId = models.ForeignKey(User)
    PhoneNumber = models.CharField(max_length=15)
    MobileOperatorId = models.ForeignKey(MobileOperators)
    ProductId = models.ForeignKey(Products)
    Amount = models.IntegerField()
    Date = models.DateField(default=datetime.date.today())


class InternetProviders(models.Model):
    Name = models.CharField(max_length=50)


class InternetPay(models.Model):
    UserId = models.ForeignKey(User)
    ProductId = models.ForeignKey(Products)
    InternetProviderId = models.ForeignKey(InternetProviders)
    ContractNumber = models.CharField(max_length=15)
    Amount = models.IntegerField()
    Date = models.DateField(default=datetime.date.today())


class FlatPay(models.Model):
    UserId = models.ForeignKey(User)
    ProductId = models.ForeignKey(Products)
    AccountNumber = models.CharField(max_length=25)
    Amount = models.IntegerField()
    Date = models.DateField(default=datetime.date.today())


class Applications(models.Model):
    ApplicationName = models.CharField(max_length=50)


class UserApplication(models.Model):
    UserId = models.ForeignKey(Users)
    Application = models.ForeignKey(Applications)


class UsersKeys(models.Model):
    UserId = models.ForeignKey(User)
    Key1 = models.CharField(max_length=10)
    Key2 = models.CharField(max_length=10)
    Key3 = models.CharField(max_length=10)
    Key4 = models.CharField(max_length=10)
    Key5 = models.CharField(max_length=10)
    Key6 = models.CharField(max_length=10)
    Key7 = models.CharField(max_length=10)
    Key8 = models.CharField(max_length=10)
    Key9 = models.CharField(max_length=10)

class TransferMoneyAchive(models.Model):
    UserId = models.ForeignKey(User)
    ProductId = models.ForeignKey(Products)
    AcceptUser = models.CharField(max_length=55)
    Date = models.DateField(default=datetime.date.today())
    Amount = models.IntegerField()
