from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from collections import Counter

from .models import Lp


"""LP VIEWS"""


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['lps'] = Lp.objects.all()
        lps = context['lps']
        context['total'] = total_lp(self.request, lps)
        context['band_list'] = band_list(self.request, lps)
        context['number_of_bands'] = number_of_bands(self.request, lps)
        context['total_value'] = total_value(self.request, lps)
        context['most_common_band'] = most_common_band(self.request, lps)
        context['most_valuable'] = most_valuable(self.request, lps)

        return context


class CreateLpView(CreateView):
    model = Lp
    template_name = 'addlp.html'
    fields = ['artist', 'album_title', 'genre', 'year', 'lp_condition', 'cover_condition', 'cover_image', 'price',
              'acquisition_date', 'country', 'user']
    success_url = reverse_lazy('index')


class UpdateLpView(UpdateView):
    model = Lp
    template_name = 'addlp.html'
    fields = ['artist', 'album_title', 'genre', 'year', 'lp_condition', 'cover_condition', 'cover_image', 'price',
              'acquisition_date', 'country', 'user']
    success_url = reverse_lazy('index')


class DeleteLpView(DeleteView):
    model = Lp
    template_name = 'lp_del.html'
    success_url = reverse_lazy('index')


"""AUTH VIEWS"""


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(
                    request,
                    'signupuser.html',
                    {
                        'form': UserCreationForm(),
                        'error': 'That username has already been taken. Please choose a new name'
                    }
                )
        else:
            # Tell the user that the password do not match
            return render(request, 'signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(
                request,
                'loginuser.html',
                {
                    'form': AuthenticationForm(),
                    'error': 'Username and password are incorrect'
                }
            )
        else:
            login(request, user)
            return redirect('index')


def total_lp(request, lps):
    if len(lps) > 0:
        user_lp_list = []
        for lp in lps:
            if request.user.id == lp.user.pk:
                user_lp_list.append(lp)
        return len(user_lp_list)
    else:
        return 0


def band_list(request, lps):
    if len(lps) > 0:
        bands = []
        for lp in lps:
            if request.user.id == lp.user.pk:
                bands.append(lp.artist)
        return set(bands)
    else:
        return ""


def number_of_bands(request, lps):
    if len(lps) > 0:
        bands = []
        for lp in lps:
            if request.user.id == lp.user.pk:
                bands.append(lp.artist)
        return len(set(bands))
    else:
        return 0


def total_value(request, lps):
    total = 0
    for lp in lps:
        if request.user.id == lp.user.pk:
            total += lp.price

    return total


def most_common_band(request, lps):
    if request.user.id is None:
        return ""
    if len(lps) > 0:
        bands = []
        for lp in lps:
            if request.user.id == lp.user.pk:
                bands.append(lp.artist)
        most_common = Counter(bands).most_common()[0][0]

        return most_common
    else:
        return ""


def most_valuable(request, lps):
    if len(lps) > 0:
        most_val = ""
        for lp in lps:
            if request.user.id == lp.user.pk:
                most_val = lps[0]
                if len(lps) == 1:
                    return most_val
                for i in range(1, len(lps)):
                    if lps[i].price > most_val.price:
                        most_val = lps[i]

        return most_val
    else:
        return ""


def most_common_condition(lps):
    if len(lps) > 0:
        most_val = lps[0]
        for i in range(1, len(lps)):
            if lps[i].price > most_val.price:
                most_val = lps[i]

        return most_val
    else:
        return ""
