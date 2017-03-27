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
    Prone = models.CharField(max_length=15)

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



