from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import User,Patient,Doctor,Reports,Treatment
from .forms import FileForm , send_to_doc_Form,Register_Doc,Register_Patient
from .utils import send_email
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin


# Create your views here.
class SendToDoc(PassRequestMixin, SuccessMessageMixin, generic.CreateView):
    print("here")
    form_class = send_to_doc_Form
    template_name = 'Users/send.html'
    success_message = 'Success: Sent To Doctor.'
    success_url = reverse_lazy('reports')


def View_Treatment(request):
    Treatments = Treatment.objects.filter(Patient=request.user.Patient)
    return render(request, 'Users/Treat.html',{
        'Treatments' : Treatments
    })    


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
              }

    if not context:
        context = {
            'form': form,
        }
    print(context)
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



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def reg(request):
    return render(request, "Users/registerDoctor.html")


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        form = Register_Patient(request.POST)
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Users/registerDoctor.html", {
                "message": "Passwords must match.",
                "form" : form
            })
        if not form.is_valid():
            return render(request, "Users/registerDoctor.html",{
                "form" : form
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password,is_active = True,is_patient = True)
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
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        form = Register_Patient()
        return render(request, "Users/registerDoctor.html",{
            "form" : form
        })


def register_Doctor(request):
    if request.method == "POST":
        form = Register_Doc(request.POST)
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Users/registerDoctor.html", {
                "message": "Passwords must match.",
                "form" : form
            })
        if not form.is_valid():
            return render(request,"Users/registerDoctor.html",{
                 "form" : form
                 })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password,is_active = True,is_doctor = True)
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
                "form" : form
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    form = Register_Doc()
    return render(request,"Users/registerDoctor.html",{
        "form" : form
    })

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
        