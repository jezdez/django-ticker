from django.utils.safestring import mark_safe
from django import forms

class ForeignKeyAsTextWidget(forms.HiddenInput):

    def __init__(self, append_text, *args, **kwargs):
        self.append_text = append_text
        super(ForeignKeyAsTextWidget, self).__init__()

    def render(self, *args, **kwargs):
        field_value = super(ForeignKeyAsTextWidget, self).render(*args, **kwargs)
        return mark_safe("%s <strong>%s</strong>" % (field_value, self.append_text))
