from .models import ArticleModel
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


# Create your views here.


class ArticlesListView(ListView):
    model = ArticleModel
    context_object_name = 'articles'
    template_name = 'articles/all_articles.html'


class ArticleDetailView(DetailView):
    model = ArticleModel
    context_object_name = 'article'
    template_name = 'articles/article_detail.html'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = ArticleModel
    fields = ['title', 'description', 'image', 'content']
    success_url = reverse_lazy('articles:all-articles')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = ArticleModel
    fields = ['title', 'description', 'image', 'content']

    def get_success_url(self):
        return reverse_lazy('articles:article', kwargs={'slug': self.object.slug})

    def get_object(self, queryset=None):
        article = super().get_object(queryset)

        if article.author != self.request.user:
            raise PermissionDenied(
                'Do not have permission to change this article\'s contents')
        return article


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = ArticleModel
    context_object_name = 'article'
    template_name = 'articles/delete_form.html'
    success_url = reverse_lazy('articles:all-articles')

    def get_object(self, queryset=None):
        article = super().get_object(queryset)

        if article.author != self.request.user:
            raise PermissionDenied(
                'Do not have permission to change this article\'s contents')
        return article
