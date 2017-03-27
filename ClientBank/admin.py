from django.contrib import admin
from ClientBank.models import Users, UserInformation, ProductStatus, ProductType, Currency, Products

admin.site.register(Users)
admin.site.register(UserInformation)
admin.site.register(ProductStatus)
admin.site.register(ProductType)
admin.site.register(Currency)
admin.site.register(Products)