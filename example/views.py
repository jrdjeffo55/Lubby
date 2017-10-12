# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from forms import SignUpForm
from models import Clarify


User = get_user_model()


@login_required(login_url='/log_in/')
def user_list(request):
    """
    NOTE: This is fine for demonstration purposes, but this should be
    refactored before we deploy this app to production.
    Imagine how 100,000 users logging in and out of our app would affect
    the performance of this code!
    """
    users = User.objects.select_related('logged_in_user')
    for user in users:
        user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
    return render(request, 'example/user_list.html', {'users': users})


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            alpha = form.get_user()
            login(request, form.get_user())
            if alpha.is_staff == True:
                return redirect(reverse('example:teacher'))
            else:          
                return redirect(reverse('example:user_list'))
        else:
            print(form.errors)
    return render(request, 'example/log_in.html', {'form': form})


@login_required(login_url='/log_in/')
def log_out(request):
    logout(request)
    return redirect(reverse('example:log_in'))


def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('example:log_in'))
        else:
            print(form.errors)
    return render(request, 'example/sign_up.html', {'form': form})

def teacher(request):
    count1=Clarify.objects.filter(clear=1).count()
    count2=Clarify.objects.filter(clear=0).count()
    print count1, count2
    context = {
    'query_results' : Clarify.objects.all(),
    'users' : User.objects.select_related('logged_in_user'),
    'yes' : count1,
    'no' : count2,
    }
    return render(request, 'example/teacher.html', context)


def clarify(request):
    if request.method == "POST":
        print request.POST
        if request.POST['answer'] == 'Yes':
            answer = True
        else:
            answer = False
        me = request.user
        print answer
        print me
        Clarify.objects.create(user=me, clear=answer)
        return redirect('/')