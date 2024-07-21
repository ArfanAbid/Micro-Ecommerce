from django import forms
from .models import Product

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
