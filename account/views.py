from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm,  UserEditForm, ProfileEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.

def user_login(request):
    #requete pour le login
    if request.method == "POST":
        # requete a faire à chaque soumission 
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            # user =None si user ou pswd incorrect sinon user!= none
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authentifié '
                                        'avec succès')
                    
                else:
                    return HttpResponse('Compte desactivé')
                
            else: 
                return HttpResponse('Donnéés invalides')
    else:
        # Creer la page si on request = GET
        form = LoginForm()
    return render(request, 'account/login.html',
                  {'form': form})

@login_required #verifié lauthentification
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})
    
    
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # ceate a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the chosen password 
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the user object
            new_user.save()
            # create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
        else:
            return render(request,
                      'account/register.html',
                      {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})
    
# create a user profile

@login_required 
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil mis à jour avec succés')
        else:
            messages.error(request, 'Erreur de mis à jour du profil')
    else:
        user_form = UserEditForm(instance=request.user,
                                 data=request.GET)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.GET)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
