from django import forms
from .models import Category, Trackable

def tuplemaker(themodel):
    values=list(themodel.objects.values_list('name', flat=True).order_by('name'))
    final=[]
    for i in range (len(values)):
        final.append((values[i],values[i]))
    return final

class NewCategoryForm(forms.Form):
    name=forms.CharField(label='New Category')

    def clean_category(self):
        category=self.cleaned_data['name']
        try:
            Category.objects.get(name=category)
            message='Look at that, you already have that category!'
            raise forms.ValidationError(message)
        except:
            return category

class NewTrackableForm(forms.Form):

    name=forms.CharField(label='New Trackable')
    category=forms.ChoiceField(choices=tuplemaker(Category),label='Its Category')

    def clean_name(self):
        trackable=self.cleaned_data['name']
        try:
            Trackable.objects.get(name=trackable)
            message='Look at that, you already have that trackable!'
            raise forms.ValidationError(message)
        except:
            return trackable

class EditCategoryForm(forms.Form):
    cats=tuplemaker(Category)
    name=forms.ChoiceField(choices=cats,label="The Category")
    newname=forms.CharField(label='Its New Name')
    def clean_newname(self):
        newname=self.cleaned_data['newname']
        try:
            Category.objects.get(name=newname)
            message = 'Look at that, you already have that category!'
            raise forms.ValidationError(message)
        except:
            return newname

class EditTrackableForm(forms.Form):
    
    tracks=tuplemaker(Trackable)
    cats = tuplemaker(Category)
    
    name=forms.ChoiceField(choices=tracks,label='The Trackable')
    newname = forms.CharField(label='Its New Name')
    newcat=forms.ChoiceField(choices=cats)
    def clean_newname(self):
        newname=self.cleaned_data['newname']
        try:
            Trackable.objects.get(name=newname)
            message = 'Look at that, you already have that trackable!'
            raise forms.ValidationError(message)
        except:
            return newname
    def clean_newcat(self):
        newcat=self.cleaned_data['newcat']
        id=Category.objects.get(name=newcat).category_id
        return id


class DeleteCateogryForm(forms.Form):
    cats = tuplemaker(Category)
    name = forms.ChoiceField(choices=cats,label='The Category')

class DeleteTrackableForm(forms.Form):
    tracks = tuplemaker(Trackable)
    name = forms.ChoiceField(choices=tracks,label='The Trackable')
