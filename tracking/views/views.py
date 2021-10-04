import datetime
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

from ..forms import (
    CreateCategoryForm,
    DeleteCateogryForm,
    DeleteTrackableForm,
    EditCategoryForm,
    EditTrackableForm,
    NewTrackableForm,
    UpdateCategoryForm,
)
from ..models import Category, Cycle, Trackable
from django.views.generic import CreateView
from ..permissions import login_required_for_class


#######################################

@login_required_for_class
class TrackableCategoryManage(View):
    def edit_category(self, request, user):
        form = EditCategoryForm(request.POST)
        if form.is_valid():
            category = get_object_or_404(
                user.categories, name=form.cleaned_data["name"]
            )
            name = form.cleaned_data["newname"]
            if user.category_name_is_duplicate(name):
                raise Exception
            category.name = name
            category.save()

    def delete_category(self, request, user):
        form = DeleteCateogryForm(request.POST)
        if form.is_valid():
            category = get_object_or_404(
                user.categories, name=form.cleaned_data["name"]
            )
            category.delete()

    def add_trackable(self, request, user):
        form = NewTrackableForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if user.trackable_name_is_duplicate(name):
                raise Exception
            category = get_object_or_404(
                user.categories, name=form.cleaned_data["category"]
            )
            Trackable.objects.create(name=name, category=category)

    def edit_trackable(self, request, user):
        form = EditTrackableForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data["newname"]
            if user.trackable_name_is_duplicate(new_name):
                raise Exception
            old_category = get_object_or_404(
                user.categories, name=form.cleaned_data["oldcat"]
            )
            new_category = get_object_or_404(
                user.categories, name=form.cleaned_data["newcat"]
            )
            trackable = get_object_or_404(
                old_category.trackables, name=form.cleaned_data["name"]
            )
            trackable.name = new_name
            trackable.category = new_category
            trackable.save()

    def delete_trackable(self, request, user):
        form = DeleteTrackableForm(request.POST)
        if form.is_valid():
            category = get_object_or_404(user.categories, name=form.cleaned_data["cat"])
            trackable = get_object_or_404(
                category.trackables, name=form.cleaned_data["name"]
            )
            trackable.delete()

    def get(self, request):
        forms = {
            "newcat": CreateCategoryForm(),
            "newtrack": NewTrackableForm(),
            "editcat": EditCategoryForm(),
            "edittrack": EditTrackableForm(),
            "deletecat": DeleteCateogryForm(),
            "deletetrack": DeleteTrackableForm(),
        }
        user = request.user

        context = {
            "catdict": self.all_trackables(user=user),
            "done": "",
            "forms": forms,
        }
        return render(
            request,
            "tracking/trackables.html",
            context=context,
        )

    def post(self, request):
        form_cues = {
            "addcategory": CreateCategoryView.as_view(),
            "addtrackable": self.add_trackable,
            "editcategory": self.edit_category,
            "deletecategory": self.delete_category,
            "edittrackable": self.edit_trackable,
            "deletetrackable": self.delete_trackable,
        }
        user = request.user

        for cue, action in form_cues.items():
            if cue in request.POST:
                action(request)
                return redirect("trackable_manage")

    def all_trackables(self, user):
        all = dict()
        for category in user.categories.all():
            all[category.name] = category.trackables.all()
        return all


###### NOT VIEWS ######
def create_cycle(date, dayobj):
    id = Cycle.objects.count()
    Cycle.objects.create(idnum=id + 1, first=date)  # making new cycle
    dayobj.cycle = Cycle.objects.get(idnum=id + 1)  # adding new cycle to day object
    dayobj.save()

    # if this is not the first cycle to be created....
    if id > 0:
        a = Cycle.objects.get(idnum=id)
        a.last = date - datetime.timedelta(1)  # ending last cycle
        a.save()

        a.duration = (a.last - a.first).days  # setting last cycle duration
        a.save()
    return


#######################
