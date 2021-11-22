
from django.views.generic.base import View
from django.views.generic.edit import DeleteView
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render

from ..models import Category
from ..forms import CreateCategoryForm, UpdateCategoryForm
from periodtracker.decorators import login_required_for_class


@login_required_for_class
class CategoryListView(View):
    def get(self, request):
        user = request.user
        categories = user.categories.all()
        return render(
            request, "tracking/categories.html", context={"categories": categories}
        )


@login_required_for_class
class CategoryDetailView(View):
    def get(self, request, pk):
        user = request.user
        category = get_object_or_404(user.categories.all(), pk=pk)
        return render(
            request, "tracking/category_details.html", context={"category": category}
        )


@login_required_for_class
class CreateCategoryView(View):
    def get(self, request):
        form = CreateCategoryForm()
        return render(request, "tracking/create_category.html", context={"form": form})

    def post(self, request):
        user = request.user
        form = CreateCategoryForm(request.POST, user=user)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            category = Category.objects.create(name=name, user=user)
            return JsonResponse({'alert':f"{name} category successfully created!"})
        return render(request, "tracking/create_category.html", context={"form": form})


@login_required_for_class
class UpdateCategoryView(View):
    def post(self, request, pk):
        user = request.user
        form = UpdateCategoryForm(request.POST, user=user)
        if form.is_valid():
            category = get_object_or_404(user.categories.all(), pk=pk)
            old_name = category.name
            new_name = form.cleaned_data.get("new_name")
            category.name = new_name
            category.save()
            return JsonResponse(
                {"alert": f"{old_name} successfully changed to {new_name}!"}
            )
        return render(request, "tracking/update_category.html", context={"form": form})

    def get(self, request, pk):
        form = UpdateCategoryForm()
        return render(request, "tracking/update_category.html", context={"form": form})


@login_required_for_class
class DeleteCategoryView(DeleteView):

    model = Category
    success_url = "categories"

    def post(self, request, pk):
        user = request.user
        category = get_object_or_404(user.categories.all(), pk=pk)
        category.delete()
        return JsonResponse({"alert": f"{category.name} successfully deleted."})
