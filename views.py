from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordResetForm, 
    SetPasswordForm, PasswordChangeForm
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponse


from django.shortcuts import render

def home_view(request):
    return render(request, 'accounts/home.html')

    # This will render the home page template



from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm

def signup_view(request):
    form = SignUpForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('dashboard')

    return render(request, 'accounts/signup.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import LoginForm  # Import the LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username_or_email = form.cleaned_data['username_or_email']
        password = form.cleaned_data['password']

        # Check if the input is a username or an email
        user = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()

        if user:
            user = authenticate(request, username=user.username, password=password)  # Authenticate with username

            if user:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('dashboard')

        messages.error(request, "Invalid credentials")

    return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileUpdateForm  # Ensure you have a form for profile updates

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Correct redirect
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})

from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import ForgotPasswordForm

class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('login')
    success_message = "A password reset link has been sent to your email."



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/reset_password.html'


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Password changed successfully! Please log in again.")
            logout(request)  # Log out the user after password change
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

