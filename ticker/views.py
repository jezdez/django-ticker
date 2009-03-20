from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from ticker.models import Entry
from tagging.models import Tag, TaggedItem

def overview(request, num_latest=10, template_name='ticker/overview.html', extra_context={}):
    """Show the 10 latest entries"""
    entry_list = Entry.objects.public()[:num_latest]
    template_context = {
        'entry_list': entry_list,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context,
                              RequestContext(request))

def archive(request, template_name='ticker/archive.html', extra_context={}):
    """Shows a archive page and a list of tags"""
    entry_list = Entry.objects.public()
    tag_list = Tag.objects.cloud_for_model(Entry, steps=9, 
                                           filters={'status': Entry.STATUS_OPEN })
    template_context = {
        'entry_list': entry_list,
        'tag_list': tag_list,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context, 
                              RequestContext(request))

def archive_by_tag(request, tag, template_name='ticker/archive_by_tag.html', extra_context={}):
    """Shows a list of entries related with a specific `tag`"""
    get_object_or_404(Tag, name=tag)
    entry_list = TaggedItem.objects.get_by_model(Entry.objects.public(), [tag])
    related_tags = Tag.objects.related_for_model([tag], Entry)
    template_context = {
        'the_tag': tag,
        'related_tags': related_tags,
        'entry_list': entry_list,
    }
    template_context.update(extra_context)
    return render_to_response(template_name, template_context, 
                              context_instance=RequestContext(request))

def details(request, slug, template_name='ticker/details.html', extra_context={}):
    """Shows a details page for the given entry"""
    entry = get_object_or_404(Entry.objects.public(), slug=slug)
    template_context = {
        'entry': entry,
    }
    template_context.update(extra_context)    
    return render_to_response(template_name, template_context, 
                              RequestContext(request))
