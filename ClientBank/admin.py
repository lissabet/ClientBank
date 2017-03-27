from django.contrib import admin
from ClientBank.models import Users, UserInformation, ProductStatus, ProductType, Currency, Products, Operations, UserOperations
from  ClientBank.models import Applications, UserApplication

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