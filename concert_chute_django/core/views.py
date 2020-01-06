from django.shortcuts import render
from django.http import HttpResponse

from concert_chute_django.core.models import Concert


# Create your views here.
def home(request):
    return render(request, 'home.html', {'concerts': Concert.objects.all()})
