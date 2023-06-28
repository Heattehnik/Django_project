from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from catalog.models import Product, Article


# Create your views here.
class ProductListView(ListView):
    model = Product



def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name}\n{email}\n{message}')

    return render(request, 'catalog/contacts.html')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/card.html'


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'content',)
    success_url = reverse_lazy('catalog:articles')


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'content',)
    success_url = reverse_lazy('catalog:articles')


class ArticleListView(ListView):
    model = Article


class ArticleDetailedView(DetailView):
    model = Article
