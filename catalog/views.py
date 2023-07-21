from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.services import send_email
from catalog.forms import ProductForm
from catalog.models import Product, Article, Version
from pytils.translit import slugify


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        active_versions = Version.objects.filter(is_current_version=True).select_related('product')
        active_products = {version.product_id: version for version in active_versions}
        for product in queryset:
            product.active_version = active_products.get(product.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['products'] = queryset
        return context


@login_required
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name}\n{email}\n{message}')

    return render(request, 'catalog/contacts.html')


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/card.html'


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:catalog')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_formset = modelformset_factory(Product, form=ProductForm, extra=1)
        context_data['title'] = 'Добавить товар'
        if self.request.method == 'POST':
            context_data['formset'] = product_formset(self.request.POST)
        else:
            context_data['formset'] = product_formset()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:catalog')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_formset = modelformset_factory(Product, form=ProductForm, extra=1)
        context_data['title'] = 'Редактировать товар'
        if self.request.method == 'POST':
            context_data['formset'] = product_formset(self.request.POST)
        else:
            context_data['formset'] = product_formset()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'product.delete_product'
    success_url = reverse_lazy('catalog:catalog')


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content',)
    success_url = reverse_lazy('catalog:articles')

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'content',)
    # success_url = reverse_lazy('catalog:articles')

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view_article', args=[self.kwargs.get('pk')])


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailedView(LoginRequiredMixin, DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        if self.object.views_count == 100:
            send_email(self.object.title)
        return self.object


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('catalog:articles')
