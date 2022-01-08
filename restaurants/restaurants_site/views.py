import django
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from restaurants_site.models import Review
from restaurants_site.forms import AddReviewForm
from restaurants_site.forms import AddRestaurantForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from restaurants import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
import re
from django.template.defaultfilters import slugify

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

def signup(request: request):
    messages.get_messages(request).used = True

    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username):
            messages.error(request, "Login już istnieje")

        if User.objects.filter(email=email):
            messages.error(request, "Email już istnieje")

        if password != password2:
            messages.error(request, "Hasła nie są zgodne")

        if not re.search("^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
            messages.error(request, "Niepoprawny format adresu email")

        if not username.isalnum():
            messages.error(request, "Niepoprawny format loginu")

        if len(messages.get_messages(request)) > 0:
            return render(request, "authentication/signup.j2")

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.is_active = False

        myuser.save()

        messages.success(request, "Your account has been created")

        current_site = get_current_site(request)

        #Email
        subject = "[APP] Confirm mail!"
        message = render_to_string('email_confirmation.j2',{
            'name': myuser.first_name, 
            'domain':current_site.domain, 
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return render(request, "authentication/signin.j2")

    return render(request, "authentication/signup.j2")

def signin(request):
    messages.get_messages(request).used = True
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Niepoprawne dane")

    return render(request, "authentication/signin.j2")

def signout(request):
    logout(request)
    return HttpResponseRedirect("/")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return HttpResponseRedirect("/")
    else:
        return render(request, "authentication/activation_failed.j2")

def add_restaurant(request):
    add_restaurant_form = AddRestaurantForm(request.POST, request.FILES)

    if request.user.is_authenticated and add_restaurant_form.is_valid():
        restaurant = add_restaurant_form.save(commit= False)
        restaurant.is_active = False
        restaurant.slug = slugify(restaurant.name)

        i = 1
        while len(Restaurant.objects.filter(slug = restaurant.slug)) > 0:
            restaurant.slug = slugify(restaurant.name + str(i))
            i += 1

        restaurant.save()
    else:
        print(add_restaurant_form.errors)

    return render(request, "add_restaurant.j2", {'form': add_restaurant_form})