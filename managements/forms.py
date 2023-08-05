from django import forms
from .models import Category, Subcategory, Information, DiseaseProblem


# Category form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('image', "name_bn", "name_en")

    def save(self, commit=True):
        category = super().save(commit=False)

        if commit:
            category.save()

        return category


# Subcategory form
class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ('image', "name_bn", "name_en")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.all())

    def save(self, commit=True):
        subcategory = super().save(commit=False)

        if commit:
            subcategory.category = self.cleaned_data['category']
            subcategory.save()

        return subcategory


# Information form
class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ("name_bn", "details_bn", "name_en", "details_en")

    id = forms.IntegerField(label='ID', required=False)

    def save(self, commit=True):
        information = super().save(commit=False)

        if commit:
            information.save()

        return information


# Disease/Problem form
class DiseaseProblemForm(forms.ModelForm):
    class Meta:
        model = DiseaseProblem
        fields = ('image', "name_bn", "insects_causes_bn", "solution_bn", "warning_bn", "name_en", "insects_causes_en", "solution_en", "warning_en")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'] = forms.ModelChoiceField(queryset=Subcategory.objects.all())

    def save(self, commit=True):
        disease_problem = super().save(commit=False)

        if commit:
            disease_problem.subcategory = self.cleaned_data['subcategory']
            disease_problem.save()

        return disease_problem
