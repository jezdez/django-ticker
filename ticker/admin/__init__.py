# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from tagging.models import Tag
from ticker.models import Entry
from ticker.admin.widgets import ForeignKeyAsTextWidget, \
                                                TaggingAutocompleteWidget

class EntryAdmin(admin.ModelAdmin):
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
        'source_url',
        'tags',
        'enable_comments',
    )

    def queryset(self, request):
        """
        Zeige nur Einträge des Users oder wenn er die Rechte besitzt, alle.
        """
        if request.user.has_perm('ticker.can_change_foreign'):
            return self.model._default_manager.get_query_set()
        return self.model._default_manager.get_query_set().filter(author=request.user)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        # Autorenfeld hat als Vorauswahl den aktuellen User
        if db_field.name == "author":
            field.widget = ForeignKeyAsTextWidget(append_text="Dein Benutzername wird automatisch gespeichert")
            field.initial = self._request.user.pk
            return field

        # JQuery Autocomplete für Tags
        if db_field.name == "tags":
            field.widget = TaggingAutocompleteWidget(
                taglist=([tag.name for tag in Tag.objects.all()]))
            return field

        if db_field.name == "status":
            # #FIXME# Das hier geht schöner

            # Wenn der User kein "can_publish" recht hat, soll ihm als Auswahl
            # nur "Closed" und "Draft" angezeigt werden.
            if not self._request.user.has_perm('ticker.can_publish'):
                user_choices = ([i for i in Entry.STATUS_CHOICES \
                                 if i[0] != Entry.STATUS_OPEN])
            else:
                user_choices = Entry.STATUS_CHOICES

            # Außer der Artikel war schon "Live" gesetzt, dann soll es
            # angezeigt werden.
            if hasattr(self, '_obj') and self._obj.status == Entry.STATUS_OPEN:
                user_choices = Entry.STATUS_CHOICES

            field = forms.ChoiceField(choices=user_choices) # Bugfix: #6967
            #field.widget = forms.RadioSelect(choices=user_choices)
            return field

        # Textarea Felder einwenig größer
        if isinstance(db_field, models.TextField):
            field.widget.attrs['style'] = 'height:20em;'
            return field

        return field

    # ``formfield_for_dbfield`` hat keine Zugriff auf das Request-Objekt.
    # Darum wird es hier global in die Klasse gesetzt. Sehr häßlich. Dann
    # vielleicht doch mal Threadlocals...
    def change_view(self, request, object_id, *args, **kwargs):
        self._request = request
        self._obj = Entry.objects.get(pk=object_id)
        return super(EntryAdmin, self).change_view(request, object_id, *args, **kwargs)

    def add_view(self, request,  *args, **kwargs):
        self._request = request
        return super(EntryAdmin, self).add_view(request,  *args, **kwargs)

    def save_form(self, request, form, change):
        instance = form.save(commit=False)
        return instance

admin.site.register(Entry, EntryAdmin)
