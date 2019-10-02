from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Poster

def register(request):
    p = False
    if request.user.is_anonymous:
        p = False
    else:
        poster = Poster.objects.filter(user=request.user)
        if poster.exists():
            p = poster.first().Permissive_to_post
        else:
            p = False
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.filter(username=username).first()
            want_to_be_poster = False
            if 'I_want_to_post' in request.POST:
                if request.POST['I_want_to_post'] == "on":
                    want_to_be_poster = True
            if want_to_be_poster:
                Poster.objects.create(user=user)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form,'can_post': p})


@login_required
def profile(request):
    p = False
    if request.user.is_anonymous:
        p = False
    else:
        poster = Poster.objects.filter(user=request.user)
        if poster.exists():
            p = poster.first().Permissive_to_post
        else:
            p = False
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'can_post': p
    }

    return render(request, 'users/profile.html', context)