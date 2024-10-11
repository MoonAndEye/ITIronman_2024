import calendar

from django.http import HttpResponse
from django.utils import timezone


def index(request):
    current_year = timezone.now().year
    calendar_html = calendar.HTMLCalendar().formatyear(current_year)

    return HttpResponse(calendar_html)
