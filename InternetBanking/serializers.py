from InternetBanking.models import Users, UserInformation, UserApplication, UserOperations, Operations, Applications, Products
from rest_framework import serializers

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ('email','login','password')

class UserInformationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='login',
        queryset = Users.objects.all()
    )
    class Meta:
        model = UserInformation
        fields = ('user','FullName','Address','Phone')


