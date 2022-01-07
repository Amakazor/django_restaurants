from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from restaurants_site.models import Review
from restaurants_site.forms import AddReviewForm
from django.contrib.auth.models import User
from django.contrib import messages

from restaurants_site.models import Restaurant

def home(request: request):
    sort_direction = request.GET.get('direction')
    sort_direction = "ASC" if sort_direction == "ASC" else "DESC"

    sort_fields = ['Name', 'Average rate']

    current_order = request.GET.get('order')
    current_order = current_order if current_order is not None and current_order in sort_fields else sort_fields[1]

    restaurants = sorted(Restaurant.objects.filter(is_active = True), reverse=(True if sort_direction == "DESC" else False), key=lambda restaurant: getattr(restaurant, current_order.lower().replace(' ', '_')))

    paginator = Paginator(restaurants, 6)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    no_restaurants = len(restaurants) == 0

    return render(request, 'home.j2', {'page_object': page_object, 'sort_fields': sort_fields, 'current_sort_direction': sort_direction, 'current_order': current_order, 'no_restaurants': no_restaurants})

def restaurant(request: request, slug: str):
    try:
        restaurant = Restaurant.objects.filter(is_active = True).get(slug = slug)
    except:
        return HttpResponseRedirect("/")

    add_review_form = AddReviewForm(request.POST)

    user_logged = request.user.is_authenticated
    form_completed = request.GET.get('form_completed')

    if user_logged and add_review_form.is_valid():
        review = Review()
        review.title = add_review_form.cleaned_data['title']
        review.description = add_review_form.cleaned_data['description']
        review.rate = add_review_form.cleaned_data['rate']

        review.restaurant = restaurant
        review.user = request.user
        
        review.save()
        
        return HttpResponseRedirect("?form_completed=1")

    return render(request, 'restaurant.j2', {'restaurant': restaurant, 'review_form': add_review_form, 'user_logged': user_logged, 'form_completed': form_completed})

def redirect(request: request, catchall):
    return HttpResponseRedirect("/")

def authtest(request):
    return render(request, "authentication/authtest.html")

def signup(request: request):

    if request.method == "POST":
        username = request.POST.get('username')
        print(request.POST)
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()

        messages.success(request, "Your account has been created")

        return render(request, "authentication/signin.html")

    return render(request, "authentication/signup.html")

def signin(request):
    return render(request, "authentication/signin.html")

def signout(request):
    pass
