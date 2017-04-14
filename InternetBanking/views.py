from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from InternetBanking.serializers import UsersSerializer, UserInformationSerializer
from InternetBanking.forms import UserForm, UsersInformationFrom, UsersFrom, LoginForm
from django.contrib.auth import logout

from InternetBanking.models import Users, UserInformation, Operations

def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UsersInformationFrom(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.UserId = user

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UsersInformationFrom()

    return render(request,
                  'InternetBanking/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'user': request.user}, context)



def my_view(request):
    context = RequestContext(request)
    return render(request,
                  'base.html',
                  {'user': request.user}, context)

def profile(request):
    context = UserInformation.objects.get(UserId=request.user.id)
    return render(request,
                  'InternetBanking/profile.html',
                  {'profile': context, 'user': request.user}, RequestContext(request))

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            print(username)
            print(request.user.is_authenticated())
            return HttpResponseRedirect('/basicview/')
        else:
            return render_to_response('InternetBanking/login.html', {}, RequestContext(request))
    elif request.method == 'GET':
        return render_to_response('InternetBanking/login.html', {}, RequestContext(request))

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/basicview/')

def index(request):
    operations = Operations.objects.all()
    template = loader.get_template('InternetBanking/index.html')
    context = Context({
        'operation': operations,
    })
    return HttpResponse(template.render(context))


class UserList(generics.ListCreateAPIView):
    model = Users
    serializer_class = UsersSerializer
    queryset = Users.objects.all()
    template = loader.get_template('InternetBanking/index.html')
    context = Context({
        'latest_user_list': queryset,
    })

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

