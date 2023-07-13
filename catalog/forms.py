from django import forms
from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'preview')

    def clean_name(self):
        name = self.cleaned_data['name']
        if any(word in name.lower() for word in
               ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']):
            raise forms.ValidationError('Название продукта содержит запрещенные слова')
        return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
