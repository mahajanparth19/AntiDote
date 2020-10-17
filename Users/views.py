from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import User,Patient,Doctor,Reports,Treatment
from .forms import FileForm , send_to_doc_Form,Register_Doc,Register_Patient, LoginUserForm, RegisterUserForm
from .utils import send_email
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token

from .decorators import patient_required, doctor_required
from django.views.decorators.http import require_http_methods

# Create your views here.
@login_required
@doctor_required
def view_active_treatments(request):
    pass



@login_required()
@patient_required
def View_Treatment(request):
    Treatments = Treatment.objects.filter(Patient=request.user.Patient)
    return render(request, 'Users/Treat.html',{
        'Treatments' : Treatments
    })    

@login_required()
@patient_required
@require_http_methods(["POST"])
def send(request,nums):
    if request.method == "POST":
        files = Reports.objects.get(pk=nums)

        docs = request.POST.getlist(f'file_{nums}')
        
        for id in docs:
            if all(int(id) != doc.id for doc in files.Doctors.all()):
                d = Doctor.objects.get(pk=id)
                files.Doctors.add(d)

        for doc in files.Doctors.all():
            if str(doc.id) not in docs:
                d = Doctor.objects.get(pk=doc.id)
                files.Doctors.remove(d)
        
            
        return HttpResponseRedirect(reverse("reports")) 


@login_required()
@patient_required
def showfile(request):
    # lastfile = request.user.Patient.Reports
    form = FileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(request.user) #replace by patient

    lastfile= Reports.objects.filter(Patient=request.user.Patient)

    send_form = send_to_doc_Form(request.user.Patient)
    # treat = Treatment.objects.filter(Patient=request.user.Patient)
    # send_form.fields['Doctors'].queryset = (doc.Doctor for doc in treat )

    context = None
    if lastfile:
        context= {
              'form': form,
              'lastfile' : lastfile,
              'Send' : send_form
              }

    if not context:
        context = {
            'form': form,
            'Send' : send_form
        }

    return render(request, 'Users/files.html', context)


def rform(request,num):
    if(num == 1):
        form = Register_Patient()
    else:
        form = Register_Doc()
    
    return render(request, 'Users/form.html', {
        "form" : form
    })


def index(request):
    return render(request, "Users/index.html",)


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        log = LoginUserForm(request.POST)
        email = log.data.get("email")
        password = log.data.get("password")
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            if not user.is_active:
                return HttpResponse(f'Please confirm your email address to complete the registration')
            login(request, user)
            link = request.POST["next"]
            if link != "None":
                return HttpResponseRedirect(link)
            
            return HttpResponseRedirect(reverse("index"))
        else:   
            return render(request, "Users/login.html", {
                "message": "Invalid username and/or password.",
                "next" : request.POST["next"],
                "login" : log
            })
    else:
        log = LoginUserForm()
        if "next" in request.GET:
            url = request.GET["next"]
        else:
            url = None 
        return render(request, "Users/login.html",{
            "next" : url,
            "login" : log,
        })
        



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def reg(request):
    reg = RegisterUserForm()
    form = Register_Patient()
    return render(request, "Users/registerDoctor.html",{
        "register" : reg,
        "form" : form,
    })


def register(request):
    if request.method == "POST":
        reg = RegisterUserForm(request.POST)
        email = reg.data.get("email")
        form = Register_Patient(request.POST)
        # Ensure password matches confirmation
        password = reg.data.get("password1")
        confirmation = reg.data.get("password2")
        if password != confirmation:
            return render(request, "Users/registerDoctor.html", {
                "message": "Passwords must match.",
                "form" : form,
                "register" : reg
            })
        if not form.is_valid():
            return render(request, "Users/registerDoctor.html",{
                "form" : form,
                "register" : reg,
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password,is_active = True,is_patient = True) ### change is active to false
            user.save()
            p = form.save(commit=False)
            p.user = user
            p.save()
            current_site = get_current_site(request)
            send_email(current_site,user,p.Name)
            return render(request, "Users/confirmation.html",{
                "message" : "Confirm your email",
                "user" : user,
            })
        except IntegrityError:
            return render(request, "Users/registerDoctor.html", {
                "message": "Username already taken.",
                "form" : form,
                "register" : reg
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def register_Doctor(request):
    if request.method == "POST":
        form = Register_Doc(request.POST)
        reg = RegisterUserForm(request.POST)
        email = reg.data.get("email")
        # Ensure password matches confirmation
        password = reg.data.get("password1")
        confirmation = reg.data.get("password2")
        if password != confirmation:
            return render(request, "Users/registerDoctor.html", {
                "message": "Passwords must match.",
                "form" : form,
                "d" : True,
                "register" : reg
            })
        if not form.is_valid():
            return render(request,"Users/registerDoctor.html",{
                 "form" : form,
                 "d" : True,
                 "register" : reg
                 })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password,is_active = True,is_doctor = True) ### change is active to false
            user.save()
            d = form.save(commit=False)
            d.user = user
            d.save()
            current_site = get_current_site(request)
            send_email(current_site,user,d.Name)
            return render(request, "Users/confirmation.html",{
                "message" : "Confirm your email",
                "user" : user,
            })
        except IntegrityError:
            return render(request, "Users/registerDoctor.html", {
                "message": "Username already taken.",
                "form" : form,
                "d" : True,
                "register" : reg
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


    return HttpResponseRedirect(reverse("index"))

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
        