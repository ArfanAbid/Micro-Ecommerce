from django import forms
from .models import Product,ProductAttachment
from django.forms import modelformset_factory,inlineformset_factory

input_css_class="form-control" # declared on input.css or we can add here also


class ProductForms(forms.ModelForm):
    #name=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    
    class Meta:
        model=Product
        fields=['name', 'handle','price']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs['placeholder'] ="your name"
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class ProductUpdateForms(forms.ModelForm):
    #name=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    
    class Meta:
        model=Product
        fields=['image','name', 'handle','price']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs['placeholder'] ="your name"
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class ProductAttachmentForms(forms.ModelForm):
    class Meta:
        model=ProductAttachment
        fields=['file','name', 'is_free','active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in ['is_free','active']:
            self.fields[field].widget.attrs['class'] = input_css_class



ProductAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    form=ProductAttachmentForms,
    fields=['file','name','is_free','active'],
    extra=0,
    can_delete=False
    ) 
ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    form=ProductAttachmentForms,
    formset=ProductAttachmentModelFormSet,
    fields=['file','name','is_free','active'],
    extra=0, 
    can_delete=False
    ) 
