from django.views.generic.base import View
from django.views.generic.edit import DeleteView
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render

from ..models import Trackable
from ..forms import CreateTrackableForm, MoveTrackableForm, UpdateTrackableForm
from periodtracker.decorators import login_required_for_class


@login_required_for_class
class TrackableDetailView(View):
    def get(self, request, pk):
        user = request.user
        trackable = get_object_or_404(Trackable, pk = pk)
        if trackable not in user.trackables.all():
            return HttpResponseNotFound
        return render(
            request, "tracking/trackable_details.html", context={"trackable": trackable}
        )


@login_required_for_class
class CreateTrackableView(View):
    def get(self, request,category_pk):
        form = CreateTrackableForm()
        return render(request, "tracking/create_trackable.html", context={"form": form})

    def post(self, request, category_pk):
        user = request.user
        form = CreateTrackableForm(request.POST, user=user)
        if form.is_valid():
            category = get_object_or_404(user.categories.all(), pk=category_pk)
            name = form.cleaned_data.get("name")
            trackable = Trackable.objects.create(name=name, category=category, user=user)
            return JsonResponse({"alert": f"{name} trackable successfully created!"})
        return render(request, "tracking/create_trackable.html", context={"form": form})


@login_required_for_class
class UpdateTrackableView(View):
    def get(self, request, pk):
        form = UpdateTrackableForm()
        return render(request, "tracking/update_trackable.html", context={"form": form})

    def post(self, request, pk):
        user = request.user
        form = UpdateTrackableForm(request.POST, user=user)
        if form.is_valid():
            trackable = get_object_or_404(Trackable, pk=pk)
            if trackable not in user.trackables.all():
                return HttpResponseNotFound
            old_name = trackable.name
            new_name = form.cleaned_data.get("new_name")
            trackable.name = new_name
            trackable.save()
            return JsonResponse(
                {"alert": f"{old_name} successfully changed to {new_name}!"}
            )
        return render(request, "tracking/update_trackable.html", context={"form": form})


@login_required_for_class
class MoveTrackableView(View):
    def get(self, request, pk):
        user = request.user
        trackable = get_object_or_404(Trackable, pk=pk)
        if trackable not in user.trackables.all():
            return HttpResponseNotFound
        initial={'category':trackable.category}
        form = MoveTrackableForm(user=user, initial=initial)
        return render(request, "tracking/move_trackable.html", context={"form": form})

    def post(self, request, pk):
        user = request.user
        form = MoveTrackableForm(request.POST, user=user)
        if form.is_valid():
            trackable = get_object_or_404(Trackable, pk=pk)
            if trackable not in user.trackables.all():
                return HttpResponseNotFound
            old_category = trackable.category
            new_category = form.cleaned_data.get("category")  
            if old_category == new_category:
                return JsonResponse(
                {"alert": f"successfully saved!"}
            )

            trackable.category = new_category
            trackable.save()
            return JsonResponse(
                {"alert": f"category successfully changed from {old_category.name} to {new_category.name}!"}
            )
        return render(request, "tracking/move_trackable.html", context={"form": form})


@login_required_for_class
class DeleteTrackableView(DeleteView):

    model = Trackable
    success_url = "categories"

    def post(self, request, pk):
        user = request.user
        trackable = get_object_or_404(Trackable, pk=pk)
        if trackable not in user.trackables.all():
            return HttpResponseNotFound
        trackable.delete()
        return JsonResponse({"alert": f"{trackable.name} successfully deleted."})


