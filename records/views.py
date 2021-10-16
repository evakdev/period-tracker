from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from records.forms import LoggingForm
from records.models import Record
from records.validators import DateValidator

login_required_for_class = method_decorator(
    login_required(login_url="/users/login"), name="dispatch"
)


@login_required_for_class
class LoggingView(View):
    """Adding Logs for one day"""

    def get(self, request, date):
        self.validate_date(date)
        user = request.user
        form = LoggingForm(user=user)
        return render(request, "records/logging.html", context={"form": form})


    def post(self, request, date):
        self.validate_date(date)
        user = request.user
        form = LoggingForm(request.POST, user=user)

        if form.is_valid():
            data = form.cleaned_data
            records = []
            for trackable in data.get('trackables'):
                records.append(
                    Record(user=user, date=date, log=trackable))
            if data.get('is_bleeding'):
                bleeding = data.get('bleeding')
                records.append(
                    Record(user=user, date=date, log=bleeding))
            Record.objects.bulk_create(records)
            return JsonResponse({"alert": "successfuly added data"})
        return render(request, "records/logging.html", context={"form": form})

    def validate_date(self, date):
        validator = DateValidator(date)
        if not validator.is_valid():
           raise Http404


class DayView(View):
    """Shows logs for a single day"""

    ...
