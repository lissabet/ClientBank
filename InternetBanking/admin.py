from django.contrib import admin
from InternetBanking.models import Users, UserInformation, ProductStatus, ProductType, Currency, Products, Operations, \
    UserOperations
from InternetBanking.models import Applications, UserApplication, MobileOperators, PhoneOperation, InternetProviders, \
    InternetPay
from InternetBanking.models import FlatPay

admin.site.register(Users)
admin.site.register(UserInformation)
admin.site.register(ProductStatus)
admin.site.register(ProductType)
admin.site.register(Currency)
admin.site.register(Products)
admin.site.register(Operations)
admin.site.register(UserOperations)
admin.site.register(Applications)
admin.site.register(UserApplication)
admin.site.register(MobileOperators)
admin.site.register(PhoneOperation)
admin.site.register(InternetPay)
admin.site.register(InternetProviders)
admin.site.register(FlatPay)
