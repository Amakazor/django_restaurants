from django.core import paginator
from django.http import request
from django.shortcuts import render
from django.core.paginator import Paginator

from restaurants_site.models import Restaurant

def home(request: request):
    sort_direction = request.GET.get('direction')
    sort_direction = "ASC" if sort_direction == "ASC" else "DESC"

    sort_fields = ['Name', 'Average rate']

    current_order = request.GET.get('order')
    current_order = current_order if current_order is not None and current_order in sort_fields else sort_fields[1]

    restaurants = sorted(Restaurant.objects.all(), reverse=(True if sort_direction == "DESC" else False), key=lambda restaurant: getattr(restaurant, current_order.lower().replace(' ', '_')))

    paginator = Paginator(restaurants, 6)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, 'home.j2', {'page_object': page_object, 'sort_fields': sort_fields, 'current_sort_direction': sort_direction, 'current_order': current_order})