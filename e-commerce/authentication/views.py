from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm
# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome!')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('authentication:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'authentication/profile.html', {'form': form})