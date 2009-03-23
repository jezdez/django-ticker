from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from tagging.models import Tag
from ticker.models import Entry, EntryResource, EntryResourceType
from ticker.widgets import ForeignKeyAsTextWidget

class EntryMetadataInline(admin.StackedInline):
    model = EntryResource
    fieldsets = (
        (None, {
            'fields': (('type', 'title'), 'description', 'url')
        }),
    )

class EntryAdmin(admin.ModelAdmin):
    inlines = [EntryMetadataInline]

    list_display = (
        'title',
        'status',
        'author',
    )

    fields = (
        'author',
        'status',
        'title',
        'content',
        'content_more',
        'tags',
        'enable_comments',
    )

    def queryset(self, request):
        """
        Shows only entries which author is the current user.
        Show all entries if the user has the permission `can_change_foreign`.
        """
        if request.user.has_perm('ticker.can_change_foreign'):
            return self.model._default_manager.get_query_set()
        return self.model._default_manager.get_query_set().filter(author=request.user)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        # authors of who are not allow to edit foreign articles won't see a 
        # dropdown
        if db_field.name == "author":
            if not self._request.user.has_perm('ticker.can_change_foreign'):
                field.widget = ForeignKeyAsTextWidget(append_text=_('Your username gets saved automatically'))
            field.initial = self._request.user.pk
            return field

        if db_field.name == "status":
            # if the author has "can_publish" permissions he shall be given
            # "closed" and "draft" choices
            if not self._request.user.has_perm('ticker.can_publish'):
                user_choices = ([i for i in Entry.STATUS_CHOICES \
                                 if i[0] != Entry.STATUS_OPEN])
            else:
                user_choices = Entry.STATUS_CHOICES

            # except the article was set to be "live", then show it
            if hasattr(self, '_obj') and self._obj.status == Entry.STATUS_OPEN:
                user_choices = Entry.STATUS_CHOICES

            field = forms.ChoiceField(choices=user_choices)
            return field
        return field

    # ``formfield_for_dbfield`` has no access to the request, therefore we
    # put the request here into the global class.
    def change_view(self, request, object_id, *args, **kwargs):
        self._request = request
        self._obj = Entry.objects.get(pk=object_id)
        return super(EntryAdmin, self).change_view(request, object_id, *args, **kwargs)

    def add_view(self, request,  *args, **kwargs):
        self._request = request
        return super(EntryAdmin, self).add_view(request,  *args, **kwargs)

    def has_change_permission(self, request, obj=None):
        if not super(EntryAdmin, self).has_change_permission(request, obj):
            return False

        if obj is not None and not request.user.has_perm('ticker.can_change_foreign') \
           and request.user.pk != obj.author.pk:
            return False
        return True

admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryResourceType)
