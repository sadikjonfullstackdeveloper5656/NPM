from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView
from .forms import *
from .models import *
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


class CategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "main/add_order.html"
    success_url = reverse_lazy("index")


class CustomerView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "main/add_order.html"
    success_url = reverse_lazy("index")


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "main/add_order.html"
    success_url = reverse_lazy("index")


class IndexView(View):
    def get(self, request, cat_slug=None):
        q = request.GET.get('q')
        cats = Category.objects.all()
        if cat_slug:
            cat = get_object_or_404(Category, slug=cat_slug)
            products = Product.objects.filter(category=cat)
        elif q:
            products = Product.objects.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        else:
            products = Product.objects.all()

        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, "blog/index.html", {"products": products, "cats": cats})


class DetailProduct(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        comments = Comment.objects.filter(product=product)
        return render(request, "blog/product_detail.html", {"product": product, "comments": comments})

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.product = product
            comment.save()
            return HttpResponseRedirect(reverse('product_detail', kwargs={'pk': pk}))


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "main/add_product.html"
    success_url = reverse_lazy("index")
