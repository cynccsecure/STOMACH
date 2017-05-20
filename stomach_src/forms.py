from django import forms

from .models import Recipe
from .models import Unit
from  .models import Category


class RecipeForm(forms.ModelForm):
    description = forms.CharField(max_length=1000,
                           widget=forms.Textarea(attrs={
                               'placeholder': 'how to prepare this recipe?'
                           }), required=False)
    class Meta:
        model = Recipe
        fields = ('name', 'cook_time', 'person_amount')

class IngredientForm(forms.Form):
    name = forms.CharField(max_length=200,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'ingredient name'
                           }), required=False)
    amount = forms.IntegerField(min_value=0,required=False)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all())

class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())