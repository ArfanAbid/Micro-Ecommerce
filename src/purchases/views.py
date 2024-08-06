import random
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
# Create your views here.

from products.models import Product
from .models import Purchase

def purchase_start_view(request):
    if not request.method=="POST":
        return HttpResponseBadRequest("Only POST requests are allowed")
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("You must be logged in")
    handle=request.POST.get("handle")
    obj=Product.objects.get(handle=handle)
    purchase=Purchase.objects.create(user=request.user,product=obj)
    request.session['purchase_id']=purchase.id
    
    number=random.randint(0,1)
    if number==1:
        # success
        return HttpResponseRedirect('/purchases/success/')
        # return purchase_success_view(request) 
    else:
        # stopped
        return HttpResponseRedirect('/purchases/stopped/')
    # return HttpResponse("You're at the purchase start view.") # goto stripe api

def purchase_success_view(request):
    purchase_id=request.session.get("purchase_id")
    if purchase_id:
        purchase=Purchase.objects.get(id=purchase_id)
        purchase.completed=True
        purchase.save()
    return HttpResponse(f"You're at the purchase complete view.{purchase_id}")

def purchase_stopped_view(request):
    return HttpResponse("You're at the purchase stopped view.")
