from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from ClientBank.serializers import UsersSerializer, UserInformationSerializer
from ClientBank.forms import UserForm, UsersInformationFrom, UsersFrom

from ClientBank.models import Users, UserInformation, User


def register(request):
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
                  'ClientBank/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})





def user_login(request):

    # Если запрос HTTP POST, пытаемся извлечь нужную информацию.
    if request.method == 'POST':
        # Получаем имя пользователя и пароль, вводимые пользователем.
        # Эта информация извлекается из формы входа в систему.
                # Мы используем request.POST.get('<имя переменной>') вместо request.POST['<имя переменной>'],
                # потому что request.POST.get('<имя переменной>') вернет None, если значения не существует,
                # тогда как request.POST['<variable>'] создаст исключение, связанное с отсутствем значения с таким ключом
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Используйте Django, чтобы проверить является ли правильным
        # сочетание имя пользователя/пароль - если да, то возвращается объект User.
        user = authenticate(username=username, password=password)

        # Если мы получили объект User, то данные верны.
        # Если получено None (так Python представляет отсутствие значения), то пользователь
        # с такими учетными данными не был найден.
        if user:
            # Аккаунт активен? Он может быть отключен.
            if user.is_active:
                # Если учетные данные верны и аккаунт активен, мы можем позволить пользователю войти в систему.
                # Мы возвращаем его обратно на главную страницу.
                login(request, user)
                return HttpResponseRedirect('/basicview/')
            else:
                # Использовался не активный аккуант - запретить вход!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Были введены неверные данные для входа. Из-за этого вход в систему не возможен.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # Запрос не HTTP POST, поэтому выводим форму для входа в систему.
    # В этом случае скорее всего использовался HTTP GET запрос.
    else:
        # Ни одна переменная контекста не передается в систему шаблонов, следовательно, используется
        # объект пустого словаря...
        return render(request, 'ClientBank/login.html', {})




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
    template = loader.get_template('ClientBank/index.html')
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

