from functools import partial
from itertools import groupby
from operator import attrgetter
from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import (
    ModelMultipleChoiceField,
    ModelChoiceIterator,
)


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, field, groupby):
        self.groupby = groupby
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset
        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, objs in groupby(queryset, self.groupby):
            yield (group, [self.choice(obj) for obj in objs])


class GroupedModelChoiceField(ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        choices_groupby = kwargs.pop('choices_groupby')
        if isinstance(choices_groupby, str):
            choices_groupby = attrgetter(choices_groupby)
        elif not callable(choices_groupby):
            raise TypeError(
                "choices_groupby must either be a str or a callable accepting a single argument"
            )
        self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
        super().__init__(*args, **kwargs)


class LoggingForm(forms.Form):
    """Attention: This form is rendered manually. edit logging.html after any edit in this form."""

    bleeding = forms.ModelChoiceField(
        required=False, queryset=None, empty_label='Not Bleeding', label="Flow Level"
    )
    trackables = GroupedModelChoiceField(
        required=False,
        queryset=None,
        choices_groupby="category",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "filled-in"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["bleeding"].queryset = self.user.flow.trackables.all()
        self.fields["trackables"].queryset = self.user.trackables.all()
