from datetime import datetime, date
from django.core.exceptions import ValidationError


class DateValidator:
    def __init__(self, date_slug):
        self.cleaned_date = self.convert(date_slug)

    
    def is_valid(self):
        return self.in_present() and self.is_past_2015()
        
    def convert(self, date_slug):
        try:
            return datetime.strptime(date_slug, "%Y-%m-%d")
        except:
            raise ValidationError

    def in_present(self):
        return self.cleaned_date > datetime.now()

    def is_past_2015(self):
        return self.cleaned_date < datetime(2015, 1, 1)
