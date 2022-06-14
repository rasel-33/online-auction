from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import RegisterUserForm, UpdateProfileForm, SignInForm, ResetPasswordRequestForm, ResetPasswordForm
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
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
                gender = userdata.cleaned_data.get('gender')

            )
            subject = 'Welcome to online-auction'
            message = "Let's have an online virtual auction environment" 
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.user.email],
                fail_silently=False,
            )

            return redirect('products')

    context = {'form':userdata}
    return render(request,'accounts/registerUser.html',context)

def updateProfile(request):
    updatedata = UpdateProfileForm(request.POST)
    if request.method == 'POST':
        
        if updatedata.is_valid():
            profile = Profile.objects.get(user_id=request.user.id)
            profile.user.first_name = updatedata.cleaned_data.get('first_name')
            profile.user.last_name = updatedata.cleaned_data.get('last_name')
            profile.user.user_image = updatedata.cleaned_data.get('user_image')
            profile.user.phone = updatedata.cleaned_data.get('phone')
            profile.user.location = updatedata.cleaned_data.get('location')
            profile.user.save()
            print(profile)
            profile.save()
            return redirect('products')
    context = {'form':updatedata}
    return render(request,'accounts/updateProfile.html',context)

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
                return redirect('products')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")

    context = {'form':signinForm}
    return render(request,'accounts/signIn.html',context)

def logoutUser(request):
    logout(request)
    return redirect('signin-user')

def password_reset_request_view(request):
    form = ResetPasswordRequestForm()
    if request.method =='POST':
        resetCredential = request.POST['email']
        # print(resetCredential)
        if User.objects.filter(email__iexact=resetCredential).exists():
            user = User.objects.get(email=resetCredential)

            token = default_token_generator.make_token(user)
            subject= "Reset Password-Online-auction"
            message= "Your password reset credentials are in this link tap this link http://127.0.0.1:8000/accounts/reset_password/"+token+"/"+user.email + "/ to change your password"
            # print(resetCredential)
            # "http://127.0.0.1:8000/accounts/change-password/"+token+"/"+user.email+
            # subject = "Reset Password Online-auction"
            # message = "Your password reset credentials are in this link tap this link to change your password"
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
    context ={'form':form}
    return render(request,'accounts/passwordResetRequest.html',context)

def changePassword(request,token,email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("Signature invalid")
    except User.MultipleObjectsReturned:
        return HttpResponse("Signature invalid")
    form = ResetPasswordForm()
    if user is not None:
        token_is_valid = default_token_generator.check_token(user,token)
        if token_is_valid:
            if request.method == "POST":
                form = ResetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data.get('password')
                    user.set_password(password)
                    user.save()
                    messages.success(request,"Password was reseted")
                    return redirect('products')

            context = {'form':form}
            return render(request,'accounts/changePassword.html',context)
    return HttpResponse("Signature invalid")

    

def linkSentView(request):
    return render(request,'accounts/linkSent.html')
