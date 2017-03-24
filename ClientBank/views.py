from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt

from ClientBank.forms import UsersFrom

from ClientBank.models import Users


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