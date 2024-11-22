from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm

@login_required
def merchant_dashboard(request):
    if not request.user.is_merchant:
        return redirect('dashboard')
    products = request.user.products.all()
    return render(request, 'merchant/dashboard.html', {'products': products})

@login_required
def add_product(request):
    if not request.user.is_merchant:
        return redirect('dashboard')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.merchant = request.user
            product.save()
            return redirect('merchant_dashboard')
    else:
        form = ProductForm()
    return render(request, 'merchant/add_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = Product.objects.get(pk=pk, merchant=request.user)
    product.delete()
    return redirect('merchant_dashboard')
