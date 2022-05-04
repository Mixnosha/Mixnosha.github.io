from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
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
        'title': 'Rock'
    }
    if request.POST.get('connect'):
        username = request.user.get_username()
        room_id = request.POST['connect_loby']
        UserGame.objects.create(username=username, room_id=room_id)
        return redirect('game')
    elif request.POST.get('create_loby'):
        number_lobbi = randint(100, 999)
        context['number_lobbi'] = number_lobbi
        username = request.user.get_username()
        room_id = number_lobbi
        UserGame.objects.create(username=username, room_id=room_id)
        return redirect('game')
    return render(request, 'rockPaper/rock.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('login')


def game(request):
    context = {
        'title': 'game'
    }
    user = UserGame.objects.filter(username=request.user.get_username())[0]
    room_id = user.room_id
    context['room_id'] = room_id
    enemy = UserGame.objects.filter(room_id=room_id)
    for e in enemy:
        if e.username != user.username:
            enemy = e
            context['enemy'] = e.username
    if request.POST.get('game_start'):
        el = randint(0, 100)
        user.select_el = el
        user.save()
        context['el'] = el
        if enemy.select_el:
            context['enemy_el'] = enemy.select_el
            if el > enemy.select_el:
                context['winner'] = user.username
            else:
                context['winner'] = enemy.username
                user.select_el = None
                enemy.select_el = None
                user.save()
                enemy.save()
    return render(request, 'rockPaper/game.html', context=context)
