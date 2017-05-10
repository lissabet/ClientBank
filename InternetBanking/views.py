import csv
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext
from InternetBanking.forms import UserForm, UsersInformationFrom
from InternetBanking.forms import ProductForm, PhoneOperationForm
from InternetBanking.models import UserInformation, Operations, Products, ProductStatus, UsersKeys
from InternetBanking.models import PhoneOperation, FlatPay, InternetPay, User
from InternetBanking.forms import InternetPayForm, FlatPayForm, KeyForm, LoginForm
from InternetBanking.forms import ChangePassword, RecoverCodeForm, NewPasswordForm
import random, datetime
from django.core.mail import send_mail

i = 0
name = ''


def register(request):
    context = RequestContext(request)
    registered = False
    message = ''
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UsersInformationFrom(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() and user_form:

            user = user_form.save()

            user.set_password(user.password)
            emails = User.objects.filter(email=user.email)
            logins = User.objects.filter(username=user.username)
            if emails != []:
                message = 'Пользователь с таким email уже существует'
            elif logins != []:
                message = 'Пользователь с таким логином уже существует'
            else:
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

                userKey = UsersKeys(UserId=user, Key1=keys[0], Key2=keys[1], Key3=keys[2], Key4=keys[3], Key5=keys[4],
                                    Key6=keys[5], Key7=keys[6], Key8=keys[7], Key9=keys[8])
                userKey.save()
                mail_message = 'Welcome, {0}, to out Internet-Banking ESBBank!\n' \
                               'We send for you your private keys. Please, save them and do not show anybody!' \
                               '\n'.format(
                    user.username) + 'Key1: {0} \n Key2: {1} \n Key3: {2} \n Key4: {3} \n Key5: {4} \n ' \
                                     'Key6: {5} \n Key7: {6} \n' \
                                     'Key8: {7} \n Key9: {8} '.format(keys[0], keys[1], keys[2], keys[3], keys[4],
                                                                      keys[5],
                                                                      keys[6], keys[7],
                                                                      keys[8])

                receiverEmail = '{0}'.format(user.email)

                send_mail('ESbank keys for your banking', mail_message, 'Do not reply <do_not_replay@domain.com>',
                          [receiverEmail],
                          fail_silently=False)

                registered = True


        else:
            message = "Неккоректно введены данные"

    else:
        user_form = UserForm()
        profile_form = UsersInformationFrom()

    return render(request,
                  'InternetBanking/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered,
                   'user': request.user,
                   'message': message,
                   }, context)


def keysView(request):
    context = RequestContext(request)
    listKeys = UsersKeys.objects.last()
    return render(request, 'InternetBanking/keys.html', {'listKeys': listKeys,
                                                         'user': request.user}, context)


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


@login_required(login_url='/basicview/login/')
def operations(request):
    context = RequestContext(request)
    key_form = KeyForm()
    phone_form = PhoneOperationForm(eventUser=request.user)
    pay_form = InternetPayForm(eventUser=request.user)
    pay_flat = FlatPayForm(eventUser=request.user)
    global i
    i = random.randint(1, 9)
    return render(request,
                  'InternetBanking/operations.html',
                  {'user': request.user,
                   'key_form': key_form,
                   'phone_form':phone_form,
                   'pay_form': pay_form,
                   'pay_flat':pay_flat,
                   'Number':i}, context)


def export_phone(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export.csv'

        writer = csv.writer(response)
        writer.writerow(['Дата', 'Номер Телефона', 'Сумма', 'Мобильный оператор', 'Номер продукта'])
        pays = PhoneOperation.objects.filter(UserId=request.user)
        for rows in pays:
            writer.writerow([rows.Date, rows.PhoneNumber, rows.Amount, rows.MobileOperatorId.Name,
                             rows.ProductId.ContractNumber])
        return response
    except (Exception):
        print(Exception.__dict__)
        return HttpResponseRedirect('/basicview/')


def export_internet(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export_internet_operations.csv'
        writer = csv.writer(response)
        writer.writerow(['Дата', 'Интернет Провайдер', 'Номер Договора', 'Сумма Оплаты', 'Номер продукта'])
        pays = InternetPay.objects.filter(UserId=request.user)
        for rows in pays:
            writer.writerow(
                [rows.Date, rows.InternetProviderId.Name, rows.ContractNumber, rows.Amount,
                 rows.ProductId.ContractNumber])
        return response
    except Exception:
        print(Exception.__dict__)
        return HttpResponseRedirect('/basicview/')


def export_flatpay(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export_flat_pay_operations.csv'
        writer = csv.writer(response)
        writer.writerow(['Дата', 'Номер лицевого счета', 'Сумма Оплаты', 'Номер продукта'])
        pays = FlatPay.objects.filter(UserId=request.user)
        for rows in pays:
            writer.writerow(
                [rows.Date, rows.AccountNumber, rows.Amount, rows.ProductId.ContractNumber])
        return response
    except (Exception):
        print(Exception.__dict__)
        return HttpResponseRedirect('/basicview/')


def CreateProduct(request):
    context = RequestContext(request)
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            userProduct = Products.objects.filter(AccountNumber=request.user.id).filter(TypeId=product.TypeId).filter(
                CurrencyId=product.CurrencyId)
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
        phone_form = PhoneOperationForm(data=request.POST, eventUser=request.user)
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
                Products.objects.filter(pk=balans[0].id).update(Balance=balans[0].Balance - int(pay.Amount))
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
    context = RequestContext(request)
    global i
    if request.method == 'POST':
        pay_form = InternetPayForm(data=request.POST, eventUser=request.user)
        key_form = KeyForm(data=request.POST)
        userKey = UsersKeys.objects.filter(UserId=request.user)
        field = 'Key{}'.format(i)

        if pay_form.is_valid() and key_form.is_valid():
            pay = pay_form.save(commit=False)
            key = key_form.cleaned_data.get('Key')
            balance = Products.objects.filter(ContractNumber=pay.ProductId.ContractNumber)
            if balance[0].Balance >= pay.Amount and key == userKey.values('{}'.format(field))[0][field]:
                pay.UserId = request.user
                pay.save()
                Products.objects.filter(pk=balance[0].id).update(Balance=balance[0].Balance - int(pay.Amount))
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

    return render(request, 'InternetBanking/internet_pay.html', {'pay_form': pay_form,
                                                                 'user': request.user,
                                                                 'key_form': key_form,
                                                                 'Number': i}, context)


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
            if balance[0].Balance >= pay.Amount and pay.Amount > 0 and key == userKey.values('{}'.format(field))[0][
                field]:
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


@login_required(login_url='/basicview/login/')
def profile(request):
    context = UserInformation.objects.get(UserId=request.user.id)
    products = Products.objects.filter(AccountNumber=request.user.id)
    user_profile = UserInformation.objects.filter(UserId=request.user)[0]
    user = User.objects.get(pk= request.user.id)
    user_form = UserForm(instance=user)
    form = UsersInformationFrom(instance=user_profile)
    product_form = ProductForm()
    date = datetime.date.today()
    for prod in products:
        if prod.EndContractDate >= date:
            Products.objects.filter(pk=prod.id).update(StatusId=2)
    return render(request,
                  'InternetBanking/profile.html',
                  {'profile': context,
                   'user': request.user,
                   'products': products,
                   'date': date,
                   'form': form,
                   'product_form': product_form,
                   'user_form':user_form}, RequestContext(request))


def user_login(request):
    context = RequestContext(request)
    identity = False
    message = "Введен неверный логин или пароль"
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid() and request.POST.get('username') != "Логин" and request.POST.get('password') != "Пароль":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/basicview/')
            else:
                return render(request,
                              'InternetBanking/login.html',
                              {"message": message}, context)

        else:
            return render(request,
                          'InternetBanking/login.html',
                          {"message": message}, context)
    else:
        form = LoginForm()
        code_form = RecoverCodeForm()
        change_form = ChangePassword()
    return render(request,
                  'InternetBanking/login.html',
                  {'form': change_form,
                   'code_form': code_form,
                   'identity': identity}, context)


def change_password(request):
    context = RequestContext(request)
    identity = False
    if request.method == 'POST':
        form = ChangePassword(data=request.POST)
        code_form = RecoverCodeForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            key = UsersKeys.objects.filter(UserId=User.objects.get(email=email)).values_list()
            i = random.randint(2, 10)
            print(key)
            if key:
                identity = True
                code = int(key[0][i]) ^ int(User.objects.get(email=email).id)
                print(User.objects.get(email=email).id)
                print(code)
                send_code = str(code) + 'i' + str(i) + 'i' + str(User.objects.get(email=email).id)
                global name
                name = User.objects.get(email=email).username
                print('name', name)
                message = 'Your code :{0}'.format(send_code)
                receiverEmail = '{0}'.format(email)
                send_mail('Recover code ESBank', message, 'Do not reply <do_not_replay@domain.com>', [receiverEmail],
                          fail_silently=False)

        else:
            print(form.errors)
    else:
        form = ChangePassword()
        code_form = RecoverCodeForm()
    return render(request,
                  'InternetBanking/change_password.html',
                  {'form': form,
                   'code_form': code_form,
                   'identity': identity}, context)


def code(request):
    context = RequestContext(request)
    identity = True
    if request.method == 'POST':
        code_form = RecoverCodeForm(data=request.POST)
        if code_form.is_valid():
            recovercode = request.POST.get('code')
            code_part = int(recovercode.split('i')[0])
            num_part = int(recovercode.split('i')[1])
            id_part = int(recovercode.split('i')[2])
            print(id_part)
            print(code_part)
            key = UsersKeys.objects.filter(UserId=User.objects.get(pk=id_part)).values_list()[0][num_part]
            print(key)
            print(str(code_part ^ id_part) == str(key))
            if (str(code_part ^ id_part)) == str(key):
                return HttpResponseRedirect('/basicview/new_password/')
        else:
            print(code_form.errors)
    else:
        code_form = RecoverCodeForm()
    return render(request,
                  'InternetBanking/change_password.html',
                  {'code_form': code_form,
                   'identity': identity}, context)


def new_password(request):
    context = RequestContext(request)
    message = ''
    if request.method == 'POST':
        password_form = NewPasswordForm(data=request.POST)
        if password_form and password_form.is_valid() and name:
            print(name)
            user = User.objects.get(username=name)
            user.set_password(request.POST.get('password'))
            user.save()
            message = 'Пароль успещно обновлен\n' \
                      'Спасибо, что используете наш Интернет-банкинг\n\n\n\n' \
                      'С Уважением, Администрация ESBank'
            receiverEmail = '{0}'.format(user.email)
            send_mail('Пароль успещно обновлен', message, 'Do not reply <do_not_replay@domain.com>', [receiverEmail],
                      fail_silently=False)
            return HttpResponseRedirect('/basicview/successfully_password/')
        else:
            message = "Пароль введен неверно"
    else:
        password_form = NewPasswordForm()
    return render(request, 'InternetBanking/Profile/new_password.html', {'form': password_form,
                                                                         'message': message}, context)


def successfully_password(request):
    id_user = User.objects.get(username=name).id
    full_name = UserInformation.objects.get(UserId=id_user).FullName
    return render(request,
                  'InternetBanking/Messeges/Successfully_password.html',
                  {'name': full_name},
                  RequestContext(request))


def archive(request):
    context = RequestContext(request)
    phone_operations = PhoneOperation.objects.filter(UserId=request.user)
    flat_pays = FlatPay.objects.filter(UserId=request.user)
    internet_operations = InternetPay.objects.filter(UserId=request.user)
    fullname = UserInformation.objects.filter(UserId=request.user)[0]
    return render(request, 'InternetBanking/archive.html', {'user': request.user,
                                                            'phone': phone_operations,
                                                            'flat': flat_pays,
                                                            'internet': internet_operations,
                                                            'userinf': fullname}, context)


@login_required
def index(request):
    operations = Operations.objects.all()
    template = loader.get_template('InternetBanking/index.html')
    context = Context({
        'operation': operations,
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def product_export(request):
    try:
        if request.method == "POST":
            num = int(request.POST["num"])
            print(num)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=exportproduct.csv'
            writer = csv.writer(response)
            writer.writerow(['Дата', 'Операция', 'Сумма Оплаты'])
            pays = PhoneOperation.objects.filter(ProductId=num)
            print(pays)
            for rows in pays:
                writer.writerow(
                    [rows.Date, 'Оплата сотового телефона {0}'.format(rows.MobileOperatorId.Name), rows.Amount])
            pays = FlatPay.objects.filter(ProductId=num)
            print(pays)
            for rows in pays:
                writer.writerow(
                    [rows.Date, 'Оплата услуг ЖКХ', rows.Amount]
                )
            pays = InternetPay.objects.filter(ProductId=num)
            for rows in pays:
                writer.writerow(
                    [rows.Date, 'Оплата Интернет провайдера {0}'.format(rows.InternetProviderId.Name),
                     rows.Amount]
                )
            return response


    except (Exception):
        print(Exception.__dict__)
        return HttpResponseRedirect('/basicview/')


def products(request):
    product = Products.objects.filter(AccountNumber=request.user)
    for prod in product:
        print(prod.StatusId)
    return render(request, 'InternetBanking/products.html', {'user:': request.user,
                                                             'product': product})


def edit(request):
    context = RequestContext(request)
    user_profile = UserInformation.objects.filter(UserId=request.user)[0]
    user = User.objects.get(pk= request.user.id)

    if request.method == 'POST':
        form = UsersInformationFrom(request.POST, instance=user_profile)
        user_form = UserForm(request.POST,instance=user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            UserInformation.objects.filter(pk=user_profile.id).update()
            User.objects.filter(pk=user.id).update()


        return HttpResponseRedirect('/basicview/profile')
    else:
        form = UsersInformationFrom(instance=user_profile)
        user_form = UserForm(instance=user)
    return render(request, 'InternetBanking/Profile/edit.html', {'user': request.user,
                                                                 'form': form,
                                                                 'user_form':user_form}, context)


def stop(request):
    if request.method == "POST":
        num = int(request.POST["num"])
        Products.objects.filter(pk=num).update(StatusId=2)
        return HttpResponseRedirect('/basicview/profile/')


def active(request):
    if request.method == "POST":
        num = int(request.POST["num"])
        Products.objects.filter(pk=num).update(StatusId=1)
        return HttpResponseRedirect('/basicview/profile/')
