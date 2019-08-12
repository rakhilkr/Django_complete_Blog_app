from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView
)

from .forms import ArticleForm
from .models import Article


class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('/')


class Login(LoginView):
    form_class = AuthenticationForm
    success_url = 'blog-home'
    template_name = 'login.html'


class BlogHomeListView(LoginRequiredMixin, ListView):
    template_name = "articles/articles_home.html"
    model = Article

    def get_queryset(self):
        articles = self.model.objects.filter(author=self.request.user)
        return articles


class ArticleDetailView(LoginRequiredMixin, DetailView):
    template_name = "articles/article.html"
    model = Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = "articles/article_create.html"
    form_class = ArticleForm

    def form_valid(self, form):
        """
        Assign the author to the request.user
        """
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog-home')


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "articles/article_update.html"
    model = Article
    form_class = ArticleForm
