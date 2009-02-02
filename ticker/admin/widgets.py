from django.utils.safestring import mark_safe
from django import forms

class ForeignKeyAsTextWidget(forms.HiddenInput):

    def __init__(self, append_text, *args, **kwargs):
        self.append_text = append_text
        super(ForeignKeyAsTextWidget, self).__init__()

    def render(self, *args, **kwargs):
        field_value = super(ForeignKeyAsTextWidget, self).render(*args, **kwargs)
        return mark_safe("%s <strong>%s</strong>" % (field_value, self.append_text))

class TaggingAutocompleteWidget(forms.TextInput):

    class Media:
        css = {
            'all': ('ticker/css/jquery.autocomplete.css',)
        }
        js = (
            'ticker/js/jquery.js',
            'ticker/js/jquery.bgiframe.min.js',
            'ticker/js/jquery.dimensions.js',
            'ticker/js/jquery.ajaxQueue.js',
            'ticker/js/jquery.autocomplete.js',
        )

    def __init__(self, taglist, *args, **kwargs):
        if not isinstance(taglist, (tuple, list)):
            raise Exception("'taglist' argument must be a list or a tuble of tag-strings")
        self.taglist = taglist
        super(TaggingAutocompleteWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        attrs['style'] = 'width: 30em;'
        field_value = super(TaggingAutocompleteWidget, self).render(name, value, attrs)
        return mark_safe("""
        %(field_value)s
        <script type="text/javascript">
        $(document).ready(function(){
            var global_taglist = new Array(
                '%(taglist)s'
            );

            $("#id_%(field_name)s").autocomplete(global_taglist, {
                width: 320,
                max: 4,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300
            });
        });
        </script>
        """ % {
            'field_name': name,
            'field_value': field_value,
            'taglist': "', '".join(self.taglist),
        })
