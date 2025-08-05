from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator
from django.shortcuts import render

def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category and category != "all":
        products = products.filter(category__iexact=category)

    # Pagination
    paginator = Paginator(products, 9)  # 9 produits par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/home.html', {
        'products': page_obj,  # ⚠️ Passe `page_obj` au lieu de `products`
        'page_obj': page_obj,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_available=True)
    return render(request, 'store/product_detail.html', {'product': product})

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

def terms(request):
    return render(request, 'store/terms.html')

def privacy(request):
    return render(request, 'store/privacy.html')

def legal_mentions(request):
    return render(request, 'store/legal_mentions.html')

