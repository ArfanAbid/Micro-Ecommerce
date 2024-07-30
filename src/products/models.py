from typing import Iterable
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import pathlib
from django.urls import reverse

PROTECTED_MEDIA_ROOT=settings.PROTECTED_MEDIA_ROOT
protected_storage=FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

# Create your models here.

class Product(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    # stripe_product_id=
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    name=models.CharField(max_length=100)
    handle=models.SlugField(unique=True)
    price=models.DecimalField(max_digits=10 ,decimal_places=2, default=9.99)
    original_price=models.DecimalField(max_digits=10 ,decimal_places=2, default=9.99)
    #stripe_price_id=
    stripe_price=models.IntegerField(default=999) # 100 * price
    price_changed_timestamp=models.DateTimeField(auto_now_add=False ,auto_now=False,blank=True,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.price != self.original_price:
            #price changed
            self.original_price=self.price
            # trigger an API request for the price
            self.stripe_price=int(self.price * 100)
            self.price_changed_timestamp=timezone.now()
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/products/{self.handle}/"
    
    def get_manage_url(self):
        return reverse('products:manage',kwargs={"handle":self.handle})
            
    def __str__(self):
        return self.name
    
def handle_product_attachment_upload(instance,filename):
    return f"products/{instance.product.handle}/attachments/{filename}"
    
class ProductAttachment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE) 
    file=models.FileField(upload_to=handle_product_attachment_upload, storage=protected_storage)
    name=models.CharField(max_length=120,blank=True,null=True)
    is_free=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self,*args, **kwargs):
        if not self.name:
            self.name=pathlib.Path(self.file.name).name
        super().save(*args, **kwargs)
    
    @property
    def display_name(self):
        return self.name or pathlib.Path(self.file.name).name
    
    def get_download_url(self):
        return reverse('products:download',kwargs={"handle":self.product.handle,"pk":self.pk}) # or make a f string 