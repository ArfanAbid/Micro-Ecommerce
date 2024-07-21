from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    user=models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    # stripe_product_id=
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
            
    def __str__(self):
        return self.name
            