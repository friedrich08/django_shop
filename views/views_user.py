from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from user.forms import CustomUserChangeForm, CustomUserCreationForm, EmailAuthenticationForm
from user.models import Role  # Importer le modèle Role

def home(request):
    return render(request, 'user/home.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Connexion réussie. Bienvenue {user.username} !")
            return redirect('home')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = EmailAuthenticationForm()

    return render(request, 'user/login.html', {'form': form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('home')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'user/profile_edit.html', {'form': form})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été changé avec succès.')
            return redirect('home')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user/password_change.html', {'form': form})

@login_required
def profile_delete(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Votre compte a été supprimé avec succès.")
        return redirect('home')

    return render(request, 'user/profile_delete.html')

def user_signup(request):
    if request.user.is_authenticated:
        messages.info(request, "Vous êtes déjà connecté.")
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Associer le rôle "user" par défaut
            role, created = Role.objects.get_or_create(role_name='user')
            user.roles = role
            user.save()
            login(request, user)
            messages.success(request, f"Inscription réussie ! Bienvenue {user.username}.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'user/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'user/profile.html')