from django.shortcuts import render, get_object_or_404
from .forms import ProductForm
from catalog.models import Product


# Create your views here.

def index(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list
    }
    return render(request, 'catalog/index.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name}\n{email}\n{message}')

    return render(request, 'catalog/contacts.html')


def product_card(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/card.html', {'product': product})
