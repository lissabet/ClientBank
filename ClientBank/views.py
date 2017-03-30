from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from ClientBank.serializers import UsersSerializer, UserInformationSerializer
from ClientBank.forms import UsersFrom

from ClientBank.models import Users, UserInformation


def index(request):
    latest_user_list = Users.objects.all()
    template = loader.get_template('ClientBank/index.html')
    context = Context({
        'latest_user_list': latest_user_list,
    })
    return HttpResponse(template.render(context))
@csrf_exempt
def add_user(request):
    template = loader.get_template('ClientBank/add_user.html')

    if request.method == 'POST':
        form = UsersFrom(request.POST)

        if form.is_valid():
            form.save(commit=True)
            form.save()
            return index(request)
        else:
            print(form.errors)
    else:
        form = UsersFrom()

    context = Context({
        'form': form
    })
    return HttpResponse(template.render(context))


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request),
        'info': reverse('info-list', request=request),
    })

class UserList(generics.ListCreateAPIView):
    model = Users
    serializer_class = UsersSerializer
    queryset = Users.objects.all()

class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Users
    serializer_class = UsersSerializer
    queryset = Users.objects.all()

class InfoList(generics.ListCreateAPIView):
    model = UserInformation
    serializer_class = UserInformationSerializer
    queryset = UserInformation.objects.all()

class InfoDetail(generics.RetrieveUpdateDestroyAPIView):
    model = UserInformation
    serializer_class = UserInformationSerializer
    queryset = UserInformation.objects.all()