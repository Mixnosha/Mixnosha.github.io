import time

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from random import randint
from rockPaper.forms import RegisterUserForms, LoginUserForm
from rockPaper.models import UserGame


class RegisterUser(CreateView):
    form_class = RegisterUserForms
    template_name = 'rockPaper/register.html'
    success_url = 'rock'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'rockPaper/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return '/'


def rock(request):
    context = {
        'title': 'Rock',
    }
    if request.POST.get('connect'):
        username = request.user.get_username()
        room_id = request.POST['connect_loby']
        try:
            if UserGame.objects.get(room_id=room_id):
                try:
                    if UserGame.objects.filter(username=username):
                        user = UserGame.objects.filter(username=username)[0]
                        user.room_id = room_id
                        user.save()
                except Exception:
                    UserGame.objects.create(username=username, room_id=room_id)
                return redirect('game')
        except Exception:
            context['error_room'] = True
            render(request, 'rockPaper/rock.html', context=context)
    elif request.POST.get('create_loby'):
        number_lobbi = randint(100, 999)
        context['number_lobbi'] = number_lobbi
        username = request.user.get_username()
        room_id = number_lobbi
        try:
            UserGame.objects.get(username=username)
            username_b = UserGame.objects.get(username=username)
            username_b.room_id = room_id
            username_b.save()
        except Exception:
            UserGame.objects.create(username=username, room_id=room_id)
        return redirect('game')

    return render(request, 'rockPaper/rock.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('register')


def game(request):
    user = UserGame.objects.filter(username=request.user.get_username())[0]
    try:
        enemy = UserGame.objects.filter(room_id=user.room_id)
        for e in enemy:
            if e.username != user.username:
                enemy = e
        context = {
            'title': 'game',
            'room_id': user.room_id,
            'rand': True,
            'enemy': enemy.username,

        }
    except Exception:
        context = {
            'title': 'game',
            'room_id': user.room_id,
            'rand': True,
        }
    if request.POST.get('game_start'):
        el = randint(0, 100)
        user.select_el = el
        user.save()
        context['el'] = el
        context['rand'] = False
    if request.POST.get('game_up'):
        try:
            if user.select_el > enemy.select_el:
                context['winner'] = user.username
                context['enemy_el'] = enemy.select_el
                context['el'] = user.select_el
                context['rand'] = False
            else:
                context['winner'] = enemy.username
                context['enemy_el'] = enemy.select_el
                context['el'] = user.select_el
                context['rand'] = False
        except Exception:
            context['enemy_no_change'] = True
            context['el'] = user.select_el
            context['rand'] = False
    if request.POST.get('restart'):
        try:
            context = {
                'title': 'game',
                'room_id': user.room_id,
                'enemy': enemy.username,
                'rand': True
            }
            user.select_el = None
            enemy.select_el = None
            user.save()
            enemy.save()
        except Exception:
            context = {
                'title': 'game',
                'room_id': user.room_id,
                'rand': True
            }
            user.select_el = None
            user.save()
    if request.POST.get('main_menu'):
        user.room_id = None
        user.select_el = None
        user.save()
        return redirect('/')
    return render(request, 'rockPaper/game.html', context=context)
