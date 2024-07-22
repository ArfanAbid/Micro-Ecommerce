from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from .models import Product
from .forms import ProductForms,ProductUpdateForms


def product_create_view(request):
    context={}
    form = ProductForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj=form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect('/products/create/')
        else:
            form.add_error(None,"You must be logged In")    
    context['form']=form    
    return render(request,'products/create.html',context)

def product_list_view(request):
    object_list = Product.objects.all()
    return render(request,'products/list.html',{"object_list":object_list})


def product_detail_view(request,handle=None):
    obj=get_object_or_404(Product, handle=handle)
    is_owner=False
    if request.user.is_authenticated:
        is_owner=obj.user == request.user
    context={"object":obj}
    if is_owner:
        form = ProductUpdateForms(request.POST or None, request.FILES or None ,instance=obj)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.save()
            # return redirect('/products/create/')

        context['form']=form    
    return render(request,'products/detail.html',context)
