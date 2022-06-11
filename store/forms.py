from dataclasses import fields
from .models import ReviewRating,product,Variation,VarientColor,VarientSize
from django.forms import ModelForm


class AddProductForm(ModelForm):
    class Meta:
        model = product
        fields = (
            "category",
            "product_name",
            "price",    
            "margin_price",
            "description",
            "image",
        )
    def __init__(self,*args, **kwargs):
        super(AddProductForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"]="form-control"


class AddVariationForm(ModelForm):
    class Meta:
        model = Variation
        fields = (
            'product',
            'varient_name',
            "sub_category",
            'color',
            'image1',
            'image2',
            'image3',
            'image4',
            # 'stock',
            'is_available'
        )
    
    def __init__(self,*args, **kwargs):
        super(AddVariationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"]="my-2 form-control"

class AddSizeForm(ModelForm):
    class Meta:
        model = VarientSize
        fields = (
            'product',
            'size',
            'stock'
        )

class  ReviewForm(ModelForm):
    class Meta:
        model = ReviewRating
        fields = (
            'subject',
            'review',
            'rating',
        )

    def __init__(self,*args, **kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"]="my-2 form-control"

