from django.db import models

class Users(models.Model):
    email = models.CharField(max_length=50)
    login = models.CharField(max_length=25)
    password = models.CharField(max_length=75)

    def __unicode__(self):
        return self.choice


class UserInformation(models.Model):
    UserId = models.ForeignKey(Users)
    FullName = models.CharField(max_length=75)
    Address = models.CharField(max_length=250)
    Phone = models.CharField(max_length=15)

    def __unicode__(self):
        return self.choice

class ProductStatus(models.Model):
    StatusName = models.CharField(max_length=20)

    def __unicode__(self):
        return self.choice

class ProductType(models.Model):
    TypeName = models.CharField(max_length=50)

    def __unicode__(self):
        return self.choice

class Currency(models.Model):
    CurrencyName = models.CharField(max_length=100)
    CurrencyCode = models.CharField(max_length=5)

    def __unicode__(self):
        return self.choice

class Products(models.Model):
    TypeId = models.ForeignKey(ProductType)
    Balance = models.IntegerField
    AccountNumber = models.CharField(max_length=25)
    ContractNumber = models.CharField(max_length=10)
    ContractDate = models.DateField
    EndContractDate = models.CharField
    StatusId = models.ForeignKey(ProductStatus)
    CurrencyId = models.ForeignKey(Currency)

    def __unicode__(self):
        return self.choice

class Operations(models.Model):
    OperationName = models.CharField(max_length=70)
    OperationCost = models.IntegerField

    def __unicode__(self):
        return self.choice

class UserOperations(models.Model):
    UserId = models.ForeignKey(Users)
    OperationId = models.ForeignKey(Operations)

    def __unicode__(self):
        return self.choice

class Applications(models.Model):
    ApplicationName = models.CharField(max_length=50)

    def __unicode__(self):
        return self.choice

class UserApplication(models.Model):
    UserId = models.ForeignKey(Users)
    Application = models.ForeignKey(Applications)

    def __unicode__(self):
        return self.choice
