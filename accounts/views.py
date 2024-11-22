

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# defin login required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import CustomUser
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to a homepage or dashboard after login
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            # Automatically log in the user after successful registration
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')  # Redirect to dashboard or wherever you like
        else:
            messages.error(request, "There was an error in your form. Please check the fields.")
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the database
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect to login after successful registration
        else:
            messages.error(request, "There was an error creating your account. Please try again.")
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard_view(request):
    # Check if the user is a superuser (admin)
    if request.user.is_superuser:
        total_users = CustomUser.objects.count()
        return render(request, 'accounts/admin_dashboard.html')
    
    # Otherwise, render the user-specific dashboard
    return render(request, 'accounts/user_dashboard.html', {'user': request.user})

@login_required
def admin_dashboard(request):
    total_users = CustomUser.objects.count()
    return render(request, 'accounts/admin_dashboard.html', {'total_users': total_users})
