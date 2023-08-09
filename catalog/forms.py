from django import forms
from catalog.models import Product


class ProductForm(forms.ModelForm):
    '''Формы для CREATE и UPDATE'''
    class Meta:
        model = Product
        fields = ('name', 'description', 'picture', 'category', 'price',)

    def clean_name(self):
        '''Валидация названия продукта'''
        cleaned_data = self.cleaned_data['name']
        banned_worlds = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

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

