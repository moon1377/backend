from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import UploadProduct

@login_required(login_url="/users/login/")
def product_list_view(request):
    if request.method == 'POST':
        form = UploadProduct(request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            return redirect('product:home')
    else:
        form = UploadProduct()
    
    # Obtener lista de productos
    product_list = Product.objects.all()[:20]
    
    return render(request, "product/list.html", {
        "product_list": product_list,
        "form": form
    })