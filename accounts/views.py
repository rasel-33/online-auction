from django.shortcuts import render,redirect
from .forms import RegisterUserForm, UpdateProfileForm, SignInForm
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
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
            Profile.objects.create(
                user_id=user.id,
                user_type=userdata.cleaned_data.get('user_type'),
                gender = userdata.cleaned_data.get('gender')

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
