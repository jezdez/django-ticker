# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from ticker.models import Entry
from ticker.forms import BetterFreeThreadedCommentForm
from tagging.models import Tag, TaggedItem

def overview(request, page=None, per_page=10, template_name='ticker/overview.html'):
    entry_list = Entry.objects.public()

    return render_to_response(template_name, {
        'entry_list': entry_list,
        'per_page': per_page,
    }, RequestContext(request))

def archive(request, template_name='ticker/archive.html'):

    entry_list = Entry.objects.public()
    tag_list = Tag.objects.cloud_for_model(Entry, steps=9, filters={
        'status': Entry.STATUS_OPEN
    })
    return render_to_response(template_name, {
        'entry_list': entry_list,
        'tag_list': tag_list,
    }, RequestContext(request))

def archive_by_tag(request, tag, template_name='ticker/archive_by_tag.html'):

    # Prüfe ob der Tag auch existiert
    get_object_or_404(Tag, name=tag)

    entry_list = TaggedItem.objects.get_by_model(Entry.objects.public(), [tag])
    related_tags = Tag.objects.related_for_model([tag], Entry)

    return render_to_response(template_name, {
        'the_tag': tag,
        'related_tags': related_tags,
        'entry_list': entry_list,
    }, context_instance=RequestContext(request))


def details(request, slug, template_name='ticker/details.html'):
    entry = get_object_or_404(Entry.objects.public(), slug=slug)
    return render_to_response(template_name, {
        'entry': entry,
        'is_detail': True,
        'comment_form': BetterFreeThreadedCommentForm(),
    }, RequestContext(request))
