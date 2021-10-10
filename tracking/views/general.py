from django.views.generic.base import View
from django.shortcuts import render


class RedirectView(View):
    def get(self,request):
        context = request.json
        return render(request, "redirect.html", context=context)
