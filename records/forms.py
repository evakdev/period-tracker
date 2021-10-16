from functools import partial
from itertools import groupby
from operator import attrgetter
from django import forms
from django.forms.models import ModelChoiceField, ModelChoiceIterator


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

class GroupedModelChoiceField(ModelChoiceField):
    def __init__(self, *args, choices_groupby, **kwargs):
        if isinstance(choices_groupby, str):
            choices_groupby = attrgetter(choices_groupby)
        elif not callable(choices_groupby):
            raise TypeError('choices_groupby must either be a str or a callable accepting a single argument')
        self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
        super().__init__(*args, **kwargs)


class LoggingForm(forms.Form):
    """Attention: This form is rendered manually. edit logging.html after any edit in this form."""
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)
        self.fields['bleeding'].queryset = self.user.flow.trackables.all()
        self.fields['trackables'].queryset = self.user.trackables

    is_bleeding=forms.BooleanField(required=False, label='Are you experiencing bleeding?')
    bleeding = forms.ModelChoiceField(queryset=None, empty_label=None, label='Flow Level')
    trackables = GroupedModelChoiceField(queryset=None,choices_groupby='category',empty_label=None,widget = forms.CheckboxSelectMultiple(attrs={'class':'accordion_form'}))


    def as_table(self):
        "Return this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row='<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td></tr>',
            error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='</td></tr>',
            help_text_html='<br><span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )
