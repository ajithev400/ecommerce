from dataclasses import fields
from .models import ReviewRating,product,Variation,VarientColor
from django.forms import ModelForm


class AddProductForm(ModelForm):
    class Meta:
        model = product
        fields = (
            "category",
            "sub_category",
            "product_name",
            "slug",
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
            'slug',
            'color',
            'size',
            'image1',
            'image2',
            'image3',
            'image4',
            'margin_price',
            'price',
            # 'stock',
            'is_available'
        )
    
    def __init__(self,*args, **kwargs):
        super(AddVariationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"]="my-2 form-control"


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

