from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelChoiceField

from .models import Category, Trackable


class CreateCategoryForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)

    class Meta:
        model = Category
        fields = ('name',)
        labels = {'name': ""}

    def clean_name(self):
        name=self.cleaned_data.get('name')
        name_exists = self.user.category_name_is_duplicate(name)
        if name_exists:
            raise ValidationError('You already have a category with that name.')
        return name

class UpdateCategoryForm(forms.Form):

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)

    new_name = forms.CharField(max_length=100, min_length=1, label="")

    def clean_new_name(self):
        new_name=self.cleaned_data.get('new_name')
        new_name_exists = self.user.category_name_is_duplicate(new_name)
        if new_name_exists:
            raise ValidationError('You already have a category with that name.')
        return new_name

    class Meta:
        model = Category
        fields = ('new_name',)

class CreateTrackableForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)

    class Meta:
        model = Trackable
        fields = ('name',)

    def clean_name(self):
        name=self.cleaned_data.get('name')
        name_exists = self.user.trackable_name_is_duplicate(name)
        if name_exists:
            raise ValidationError('You already have a trackable with that name.')
        return name

class UpdateTrackableForm(forms.Form):

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)

    new_name = forms.CharField(max_length=100, min_length=1)

    def clean_new_name(self):
        new_name=self.cleaned_data.get('new_name')
        new_name_exists = self.user.trackable_name_is_duplicate(new_name)
        if new_name_exists:
            raise ValidationError('You already have a trackable with that name.')
        return new_name

    class Meta:
        model = Trackable
        fields = ('new_name',)


class MoveTrackableForm(forms.Form):

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)
        self.fields['category'].queryset = self.user.categories.all()

    category = ModelChoiceField(queryset=None)

    class Meta:
        model = Trackable
        fields = ('category',)


class DeleteTrackableForm(forms.ModelForm):
    class Meta:
        model = Trackable
        fields = ('name',)

