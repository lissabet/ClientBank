from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from rest_framework import generics
from InternetBanking.serializers import UsersSerializer, UserInformationSerializer
from InternetBanking.forms import UserForm, UsersInformationFrom
from django.contrib.auth import logout
from InternetBanking.forms import ProductForm, PhoneOperationForm
from InternetBanking.models import Users, UserInformation, Operations, Products, ProductStatus, UsersKeys
from InternetBanking.forms import InternetPayForm, FlatPayForm, KeyForm
import random, datetime


i= 0

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


            keys = []
            for k in range(9):
                key = ''
                key += str(random.randint(5525, 25896))
                while len(key) < 10:
                    key += str(random.randint(0, 9))
                keys.append(key)

            print(keys)
            userKey = UsersKeys(UserId=user,Key1= keys[0],Key2= keys[1],Key3= keys[2],Key4 =keys[3],Key5= keys[4],Key6 = keys[5],Key7= keys[6],Key8= keys[7],Key9 =keys[8])
            userKey.save()



            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UsersInformationFrom()

    return render(request,
                  'InternetBanking/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'user': request.user,
                   }, context)


def keys(request):
    context = RequestContext(request)
    listKeys = UsersKeys.objects.last()
    return render(request,'InternetBanking/keys.html',{'listKeys': listKeys,
                                                       'user':request.user},context)

def warring(request):
    context = RequestContext(request)
    return render(request,
                  'InternetBanking/warring.html',
                  {'user': request.user}, context)

def nomoney(request):
    context = RequestContext(request)
    return render(request,
                  'InternetBanking/nomoney.html',
                  {'user': request.user}, context)
def operations(request):
    context = RequestContext(request)
    return render(request,
                  'InternetBanking/operations.html',
                  {'user': request.user}, context)


def CreateProduct(request):
    context = RequestContext(request)
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            userProduct = Products.objects.filter(AccountNumber=request.user.id).filter(TypeId=product.TypeId).filter(CurrencyId=product.CurrencyId)
            if userProduct.count() == 0:
                product.AccountNumber = request.user
                product.StatusId = ProductStatus.objects.get(pk=1)
                product.ContractNumber = int(random.randint(1555, 1555555) * random.randint(2, 555) / 55)
                product.save()
                return HttpResponseRedirect('/basicview/profile/')
            else:
                return HttpResponseRedirect('/basicview/warring/')

        else:
            print(product_form.errors)
    else:
        product_form = ProductForm()
    return render(request,
                  'InternetBanking/create_product.html',
                  {'product_form': product_form,
                   'user': request.user}, context)


def phone_operation(request):
    context = RequestContext(request)
    global i
    if request.method == 'POST':
        phone_form = PhoneOperationForm(data=request.POST,eventUser=request.user)
        key_form = KeyForm(data=request.POST)
        userKey = UsersKeys.objects.filter(UserId=request.user)
        field = 'Key{}'.format(i)
        if phone_form.is_valid() and key_form.is_valid():
            pay = phone_form.save(commit=False)
            key = key_form.cleaned_data.get('Key')
            balans = Products.objects.filter(ContractNumber=pay.ProductId.ContractNumber)
            if balans[0].Balance >= pay.Amount and key == userKey.values('{}'.format(field))[0][field]:
                pay.UserId = request.user
                pay.save()
                Products.objects.filter(pk = balans[0].id).update(Balance = balans[0].Balance - int(pay.Amount))
                return HttpResponseRedirect('/basicview/profile/')
            else:
                return HttpResponseRedirect('/basicview/nomoney')

        else:
            print(phone_form.errors)
    else:
        phone_form = PhoneOperationForm(eventUser=request.user)
        key_form = KeyForm()
        global i
        i = random.randint(1, 9)
    return render(request,
                  'InternetBanking/phone_operation.html',
                  {'phone_form': phone_form,
                   'user': request.user,
                   'key_form': key_form,
                   'Number': i
                   }, context)




def internet_pay(request):
    context =RequestContext(request)
    global i
    if request.method == 'POST':
        pay_form = InternetPayForm(data=request.POST, eventUser=request.user)
        key_form = KeyForm(data=request.POST)
        userKey = UsersKeys.objects.filter(UserId=request.user)
        field ='Key{}'.format(i)


        if pay_form.is_valid() and key_form.is_valid():
            pay = pay_form.save(commit=False)
            key = key_form.cleaned_data.get('Key')
            balance = Products.objects.filter(ContractNumber=pay.ProductId.ContractNumber)
            if balance[0].Balance >= pay.Amount and key == userKey.values('{}'.format(field))[0][field]:
                pay.UserId = request.user
                pay.save()
                Products.objects.filter(pk=balance[0].id).update(Balance= balance[0].Balance - int(pay.Amount))
                return HttpResponseRedirect('/basicview/profile/')
            else:
                return HttpResponseRedirect('/basicview/nomoney/')
        else:
            print(pay_form.errors)
    else:
        pay_form = InternetPayForm(eventUser=request.user)
        key_form = KeyForm()
        global i
        i = random.randint(1, 9)

    return render(request,'InternetBanking/internet_pay.html',{'pay_form':pay_form,
                                                                  'user': request.user,
                                                               'key_form':key_form,
                                                               'Number':i}, context)


def flat_pay(request):
    context = RequestContext(request)
    global i
    if request.method == 'POST':
        pay_form = FlatPayForm(data=request.POST, eventUser=request.user)
        key_form = KeyForm(data=request.POST)
        userKey = UsersKeys.objects.filter(UserId=request.user)
        field = 'Key{}'.format(i)
        if pay_form.is_valid() and key_form.is_valid():
            pay = pay_form.save(commit=False)
            key = key_form.cleaned_data.get('Key')
            balance = Products.objects.filter(ContractNumber=pay.ProductId.ContractNumber)
            if balance[0].Balance >= pay.Amount and pay.Amount > 0 and key == userKey.values('{}'.format(field))[0][field]:
                pay.UserId = request.user
                pay.save()
                Products.objects.filter(pk=balance[0].id).update(Balance=balance[0].Balance - int(pay.Amount))
                return HttpResponseRedirect('/basicview/profile/')
            else:
                return HttpResponseRedirect('/basicview/nomoney/')
        else:
            print(pay_form.errors)
    else:
        pay_form = FlatPayForm(eventUser=request.user)
        key_form = KeyForm()
        global i
        i = random.randint(1, 9)
    return render(request, 'InternetBanking/flat_pay.html', {'pay_form': pay_form,
                                                                 'user': request.user,
                                                             'key_form': key_form,
                                                             'Number': i
                                                             }, context)

def my_view(request):
    context = RequestContext(request)
    return render(request,
                  'base.html',
                  {'user': request.user}, context)

def profile(request):
    context = UserInformation.objects.get(UserId=request.user.id)
    products = Products.objects.filter(AccountNumber=request.user.id)
    date = datetime.date.today()
    for prod in products:
        if prod.EndContractDate >= date:
            Products.objects.filter(pk= prod.id).update(StatusId=2)
    return render(request,
                  'InternetBanking/profile.html',
                  {'profile': context,
                   'user': request.user,
                   'products': products,
                   'date': date}, RequestContext(request))


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
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
        'user': request.user,
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

