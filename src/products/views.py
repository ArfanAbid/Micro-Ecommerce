import mimetypes # it will guess the content type of any given file

from django.shortcuts import render,redirect,get_object_or_404
from django.http import FileResponse,HttpResponseBadRequest
# Create your views here.
from .models import *
from .forms import ProductForms,ProductUpdateForms,ProductAttachmentInlineFormSet


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


def product_manage_detail_view(request,handle=None):
    obj=get_object_or_404(Product, handle=handle)
    attachments=ProductAttachment.objects.filter(product=obj)
    is_manager=False
    if request.user.is_authenticated:
        is_manager=obj.user == request.user
    context={"object":obj}
    if not is_manager:
        return HttpResponseBadRequest()
    form = ProductUpdateForms(request.POST or None, request.FILES or None ,instance=obj)
    formset=ProductAttachmentInlineFormSet(request.POST or None, request.FILES or None, queryset=attachments)
    
    if form.is_valid() and formset.is_valid():
        instance=form.save(commit=False)    
        instance.save()
        formset.save(commit=False)
        for _form in formset:
            id_delete=_form.cleaned_data.get('DELETE')
            try:
                attachments_obj=_form.save(commit=False)
            except:
                attachments_obj=None    
            if id_delete:
                if attachments_obj is not None:     
                    if attachments_obj.pk:
                        attachments_obj.delete()
            else:
                if attachments_obj is not None:     
                    attachments_obj.product=instance
                    attachments_obj.save()
        return redirect(obj.get_manage_url())    
    context['form']=form   
    context['formset']=formset  
    return render(request,'products/manager.html',context)


def product_detail_view(request,handle=None):
    obj=get_object_or_404(Product, handle=handle)
    attachments=ProductAttachment.objects.filter(product=obj)
    # attachments=obj.productattachment_set.all()
    is_owner=False
    if request.user.is_authenticated:
        is_owner=request.user.purchase_set.all().filter(product=obj,completed=True).exists()
    context={"object":obj,"is_owner":is_owner,'attachments':attachments}
    return render(request,'products/detail.html',context)


def product_attachment_download_view(request,handle=None,pk=None):
    attachment=get_object_or_404(ProductAttachment,product__handle=handle,pk=pk)
    can_download=attachment.is_free or False
    if request.user.is_authenticated:
        can_download=True
    if can_download is False:
        return HttpResponseBadRequest()
    
    file=attachment.file.open(mode='rb')# cdn or S3 is preferred => object storage
    filename=attachment.file.name    
    content_type,_=mimetypes.guess_type(filename)
    response=FileResponse(file)
    response['Content-Type']=content_type or 'application/octet-stream'
    response['Content-Disposition']=f"attachment;filename={filename}"
    
    return response
