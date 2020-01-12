from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from concert_chute_django.core.models import Concert, Venue
from concert_chute_django.core.utils import upcoming_concerts


# Create your views here.
def home(request):
    return render(request, 'home.html', {'concerts': upcoming_concerts()})


def view_venue(request, pk):
    return render(request, 'view_venue.html', {
        'venue': get_object_or_404(Venue, pk=pk)
    })
