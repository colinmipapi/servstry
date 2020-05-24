from django.shortcuts import render

from track.models import GuestVisit


def confirmation_page(request, code):

    guest_visit = GuestVisit.objects.get(confirmation=code)

    if request.user.is_authenticated:
        nav = True
    else:
        nav = False

    return render(request, 'track/confirmation_page.html', {
        'guest_visit': guest_visit,
        'nav': nav,
    })
