from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView, DeleteView
from products.models import Category, Product, Manufacturer
from checkout.models import Coupon, Order, OrderItem
from django.db.models import Q
from .forms import CategoryForm, CouponForm, ManufacturerForm, OrderForm, ProductForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

class AdminProductListView(ListView):
    model = Product
    template_name = 'admin_dashboard/product_list.html'
    context_object_name = "products"
    ordering = ["-created_at"]
    queryset = Product.objects.all()
    title = "Product List"
    form_class = ProductForm
    items_per_page = 10

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['create_form'] = self.form_class()
        products = self.get_queryset()
        paginator = Paginator(products, self.items_per_page)

        page = self.request.GET.get("page", 1)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        # Pagination range logic
        page_numbers = list(paginator.page_range)
        current_page = products.number
        pagination_range = page_numbers[max(0, current_page - 3) : current_page + 2]
        context['current_page'] = current_page
        context['pagination_range'] = pagination_range
        context['page_numbers'] = page_numbers
        context['products'] = products
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.success(request, "Product created successfully.")
            return redirect('admin_product_list')
        else:
            return render(request, self.template_name, {'form': form})
    
class AdminDashboardView(TemplateView):
    template_name = 'admin_dashboard/dashboard.html'


class AdminProductDetailView(DetailView):
    model = Product
    template_name = 'admin_dashboard/product_detail.html'
    context_object_name = 'product'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_form'] = self.form_class(instance=self.object)
        return context

    def post(self,request,**kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('admin_product_detail', pk=self.object.pk)
        else:
            return render(request, self.template_name, {'form': form})

class AdminProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('admin_product_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        product_name = self.object.name
        self.object.delete()
        messages.success(request, f"Product '{product_name}' deleted successfully.")
        return HttpResponseRedirect(self.get_success_url())

class AdminCategoryListView(ListView):
    model = Category
    template_name = 'admin_dashboard/category_list.html'
    context_object_name = 'categories'
    form_class = CategoryForm
    ordering = ['name']
    title = "Category List"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(category.name)
            category.save()
            messages.success(request, "Category created successfully.")
            return redirect('admin_category_list')
        else:
            return render(request, self.template_name, {'form': form})

class AdminCategoryDetailView(DetailView):

    model = Category
    template_name = 'admin_dashboard/category_detail.html'
    context_object_name = 'category'
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_form'] = self.form_class(instance=self.object)
        return context

    def post(self,request,**kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('admin_category_detail', pk=self.object.pk)
        else:
            return render(request, self.template_name, {'form': form})
        
class AdminCategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('admin_category_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        category_name = self.object.name
        self.object.delete()
        messages.success(request, f"Category '{category_name}' deleted successfully.")
        return HttpResponseRedirect(self.get_success_url())

class AdminManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'admin_dashboard/manufacturer_list.html'
    context_object_name = 'manufacturers'
    form_class = ManufacturerForm
    ordering = ['name']
    title = "Manufacturer List"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manufacturer_form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            manufacturer = form.save(commit=False)
            manufacturer.slug = slugify(manufacturer.name)
            manufacturer.save()
            messages.success(request, "Manufacturer created successfully.")
            return redirect('admin_manufacturer_list')
        else:
            return render(request, self.template_name, {'form': form})

class AdminManufacturerDetailView(DetailView):

    model = Manufacturer
    template_name = 'admin_dashboard/manufacturer_detail.html'
    context_object_name = 'manufacturer'
    form_class = ManufacturerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_form'] = self.form_class(instance=self.object)
        return context

    def post(self,request,**kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('admin_manufacturer_detail', pk=self.object.pk)
        else:
            return render(request, self.template_name, {'form': form})
        
class AdminManufacturerDeleteView(DeleteView):
    model = Manufacturer
    success_url = reverse_lazy('admin_manufacturer_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        manufacturer_name = self.object.name
        self.object.delete()
        messages.success(request, f"Manufacturer '{manufacturer_name}' deleted successfully.")
        return HttpResponseRedirect(self.get_success_url())

class AdminOrderListView(ListView):
    model = Order
    template_name = 'admin_dashboard/order_list.html'
    context_object_name = 'orders'
    form_class = OrderForm
    ordering = ['-created']
    title = "Order List"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            messages.success(request, "Order created successfully.")
            return redirect('admin_order_list')
        else:
            return render(request, self.template_name, {'form': form})

class AdminOrderDetailView(DetailView):

    model = Order
    template_name = 'admin_dashboard/order_detail.html'
    context_object_name = 'order'
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_form'] = self.form_class(instance=self.object)
        return context

    def post(self,request,**kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('admin_order_detail', pk=self.object.pk)
        else:
            return render(request, self.template_name, {'form': form})
        
class AdminOrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('admin_order_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        category_name = self.object.name
        self.object.delete()
        messages.success(request, f"Order '{category_name}' deleted successfully.")
        return HttpResponseRedirect(self.get_success_url())

class AdminCouponListView(ListView):
    model = Coupon
    template_name = 'admin_dashboard/coupon_list.html'
    context_object_name = 'coupons'
    form_class = CouponForm
    ordering = ['-valid_from']
    title = "Coupon List"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coupon_form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon created successfully.")
            return redirect('admin_coupon_list')
        else:
            return render(request, self.template_name, {'form': form})

class AdminCouponDetailView(DetailView):

    model = Coupon
    template_name = 'admin_dashboard/coupon_detail.html'
    context_object_name = 'coupon'
    form_class = CouponForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_form'] = self.form_class(instance=self.object)
        return context

    def post(self,request,**kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('admin_coupon_detail', pk=self.object.pk)
        else:
            return render(request, self.template_name, {'form': form})
        
class AdminCouponDeleteView(DeleteView):
    model = Coupon
    success_url = reverse_lazy('admin_coupon_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        category_name = self.object.name
        self.object.delete()
        messages.success(request, f"Coupon '{category_name}' deleted successfully.")
        return HttpResponseRedirect(self.get_success_url())

