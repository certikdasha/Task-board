from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from taskbord.forms import CustomUserCreationForm, CardCreateForm
from taskbord.models import Cards


class Login(LoginView):
    template_name = 'login.html'


class Register(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class CardsListView(LoginRequiredMixin, ListView):
    model = Cards
    template_name = 'index.html'
    login_url = 'login/'


class CardCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    template_name = 'create.html'
    http_method_names = ['post']
    form_class = CardCreateForm
    success_url = '/'

    '''
        Изменить выбор в выпадашках
    '''
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        if self.request.user.is_staff:
            return super().form_valid(form=form)
        else:
            if self.object.executor == self.object.creator or not self.object.executor:
                return super().form_valid(form=form)
            else:
                return render(self.request, 'taskbord/wrong.html', {'text': 'only you can be the executor'})


class CardUpdateView(LoginRequiredMixin, UpdateView):

    model = Cards
    fields = ['text']
    template_name_suffix = '_update_form'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.user.is_staff:
            return super().form_valid(form=form)
        else:
            if self.object.creator == self.request.user:
                return super().form_valid(form=form)
            else:
                return render(self.request, 'taskbord/wrong.html', {'text': 'You are not a creator'})


class DeleteCardView(LoginRequiredMixin, DeleteView):
    model = Cards
    success_url = reverse_lazy('index')


class MoveCardView(LoginRequiredMixin, UpdateView):

    model = Cards
    fields = ['status']
    success_url = '/'












