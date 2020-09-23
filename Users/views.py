from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import User,Patient,Doctor

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage


# Create your views here.
def index(request):
     return render(request, "Users/index.html",)

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            if not user.is_active:
                return HttpResponse(f'Please confirm your email address to complete the registration')
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Users/login.html", {
                "message": "Invalid username and/or password.",
            })
    else:
        return render(request, "Users/login.html")


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["Name"]
        age = request.POST["Age"]
        gender = request.POST["Gender"]
        address = request.POST["Address"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Users/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password,is_active = False,is_patient = True)
            user.save()
            p = Patient.objects.create(user = user,Name = name, Age = age,Gender =  gender,Address =  address)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('Users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, "Users/confirmation.html",{
                "message" : "Confirm your email",
                "Email" : email 
            })
        except IntegrityError:
            return render(request, "Users/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Users/register.html")


def register_Doctor(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["Name"]
        age = request.POST["Age"]
        gender = request.POST["Gender"]
        address = request.POST["Address"]
        Specialization = request.POST["Specialization"]
        contact = request.POST["contact"]
        Qualification = request.POST["Qualification"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Users/registerDoctor.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password,is_active = False,is_doctor = True)
            d = Doctor.objects.create(user = user,Name = name, Age = age,Gender =  gender,Address =  address,Specialization=Specialization,contact=contact,Qualification=Qualification)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('Users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = email
            email_sender = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email_sender.send()
            return render(request, "Users/confirmation.html",{
                "message" : "Confirm your email",
                "Email" : email  
            })
        except IntegrityError:
            return render(request, "Users/registerDoctor.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Users/registerDoctor.html")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, "Users/confirmation.html",{
                "message" : "Thank you for your email confirmation. Now you can login your account." 
            })
    else:
        return render(request, "Users/confirmation.html",{
                "message" : "Activation link is invalid!" 
            })
        