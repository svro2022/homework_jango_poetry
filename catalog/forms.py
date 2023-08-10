from django import forms
from catalog.models import Product, Version


class StyleFormMixin:
    '''Стилизация'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    '''Формы для CREATE и UPDATE'''

    class Meta:
        model = Product
        fields = ('name', 'description', 'picture', 'category', 'price',)

    def clean_name(self):
        '''Валидация названия продукта'''
        cleaned_data = self.cleaned_data['name']
        banned_worlds = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                         'радар']

        if cleaned_data in banned_worlds:
            raise forms.ValidationError('В названии не может быть такого слова.')

        return cleaned_data

    def clean_description(self):
        '''Валидация описания продукта'''
        cleaned_data = self.cleaned_data['description']
        banned_worlds = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                         'радар']

        if cleaned_data in banned_worlds:
            raise forms.ValidationError('В описании не может быть такого слова.')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
