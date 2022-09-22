from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterUserForm, UpdateProfileForm, SignInForm, ResetPasswordRequestForm, ResetPasswordForm, \
    RequestCreditForm, RequestWithdraw
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Profile, Credit
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone


# Create your views here.


def registerUser(request):
    userdata = RegisterUserForm()
    if request.method == "POST":
        userdata = RegisterUserForm(request.POST)
        if userdata.is_valid():
            user = User.objects.create_user(username=userdata.cleaned_data.get('username'),
                                            first_name=userdata.cleaned_data.get('first_name'),
                                            last_name=userdata.cleaned_data.get('last_name'),
                                            email=userdata.cleaned_data.get('email'),
                                            password=userdata.cleaned_data.get('password')
                                            )
            profile = Profile.objects.create(
                user_id=user.id,
                user_type=userdata.cleaned_data.get('user_type'),
                gender=userdata.cleaned_data.get('gender'),
                phone=userdata.cleaned_data.get('phone'),
                location=userdata.cleaned_data.get('location')

            )
            Credit.objects.create(
                user_id=user.id,
                balance=0,
                expiry=timezone.now()
            )
            subject = 'Welcome to online-auction'
            message = "Let's have an online virtual auction environment On OnlineAuction"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.user.email],
                fail_silently=False,
            )

            return redirect('home')

    context = {'form': userdata}
    return render(request, 'accounts/registerUser.html', context)


def updateProfile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    fullname = profile.user.first_name + profile.user.last_name
    updatedata = UpdateProfileForm(initial={
        'first_name': profile.user.first_name,
        'last_name': profile.user.last_name,
        'user_image': profile.user_image,
        'phone': profile.phone,
        'location': profile.location
    })
    if request.method == 'POST':
        updatedata = UpdateProfileForm(request.POST, request.FILES)
        if updatedata.is_valid():
            profile.user.first_name = updatedata.cleaned_data.get('first_name')
            profile.user.last_name = updatedata.cleaned_data.get('last_name')
            profile.user_image = updatedata.cleaned_data.get('user_image')
            profile.phone = updatedata.cleaned_data.get('phone')
            profile.location = updatedata.cleaned_data.get('location')
            profile.user.save()
            print(profile)
            profile.save()
            return redirect('home')

    context = {'form': updatedata, 'profile': profile, 'fullname': fullname}
    return render(request, 'accounts/updateProfile.html', context)


def signinUser(request):
    signinForm = SignInForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Successfully logged in, Welcome {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    context = {'form': signinForm}
    return render(request, 'accounts/signIn.html', context)


def logoutUser(request):
    logout(request)
    return redirect('signin-user')


def password_reset_request_view(request):
    form = ResetPasswordRequestForm()
    if request.method == 'POST':
        resetCredential = request.POST['email']
        # print(resetCredential)
        if User.objects.filter(email__iexact=resetCredential).exists():
            user = User.objects.get(email=resetCredential)
            username = user.username
            token = default_token_generator.make_token(user)
            subject = "Reset Password-Online-auction"
            message = "In case you forgot your username :" + username + "\nYour password reset credentials are in this link click this link http://127.0.0.1:8000/accounts/reset_password/" + token + "/" + user.email + "/ to change your password"

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [resetCredential],
                fail_silently=False,
            )
            return redirect('link_sent')
        else:
            messages.warning(request, "No user found with Your given email or username")
            return redirect('password_reset_request')
    context = {'form': form}
    return render(request, 'accounts/passwordResetRequest.html', context)


def changePassword(request, token, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("Signature invalid")
    except User.MultipleObjectsReturned:
        return HttpResponse("Signature invalid")
    form = ResetPasswordForm()
    if user is not None:
        token_is_valid = default_token_generator.check_token(user, token)
        if token_is_valid:
            if request.method == "POST":
                form = ResetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data.get('password')
                    user.set_password(password)
                    user.save()
                    messages.success(request, "Password Reset Done!!")
                    return redirect('signin-user')

            context = {'form': form}
            return render(request, 'accounts/changePassword.html', context)
    return HttpResponse("Signature invalid")


def linkSentView(request):
    return render(request, 'accounts/linkSent.html')


def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    # print(user)
    fullname = profile.user.first_name + " " + profile.user.last_name
    creditObject = Credit.objects.get(user_id=pk)
    credit_balance = creditObject.balance
    credit_expiry = creditObject.expiry
    context = {'profile': profile, 'fullname': fullname, 'balance': credit_balance, 'expiry': credit_expiry}
    return render(request, 'accounts/myprofile.html', context)


def request_credit(request):
    form = RequestCreditForm()
    if request.method == 'POST':
        form = RequestCreditForm(data=request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            message = "The Buyer " + request.user.username + " requested Credit of " + str(amount) + "$"
            subject = "Credit Requested By BUYER"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ["shamimahammadrasel@gmail.com", "shihabahmed2312@gmail.com", "cse1705017brur@gmail.com"],
                fail_silently=False,
            )
            messages.success(request, "Credit Request Done")
            return redirect("home")
    context = {'form': form}

    return render(request, 'accounts/request_credit.html', context)


def request_credit_withdraw(request):
    form = RequestWithdraw()

    if request.method == 'POST':
        form = RequestWithdraw(data=request.POST)
        if form.is_valid():
            user_credit = Credit.objects.get(user=request.user.id)
            balance = user_credit.balance
            request_amount = form.cleaned_data['amount']
            if balance < request_amount:
                messages.info(request, "Insufficient Balance, Your Balance is " + str(
                    balance) + "$, but You requested for " + str(request_amount) + "$")

                return redirect(reverse('request_withdraw'))

            message = "The seller " + request.user.username + " is requesting withdrawal of " + str(
                request_amount) + "$"
            subject = "Withdraw requested by SELLER"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ["shamimahammadrasel@gmail.com", "shihabahmed2312@gmail.com", "cse1705017brur@gmail.com"],
                fail_silently=False,
            )
            messages.success(request, "Withdraw request will be varified, further process will be done by the admin")
            return redirect("home")
    context = {'form': form}
    return render(request, 'accounts/request_withdraw.html', context)
