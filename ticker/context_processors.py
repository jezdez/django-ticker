from django.template.defaultfilters import dictsortreversed

from tagging.models import Tag
from ticker.models import Entry

def popular_tags(request):
    poptags = Tag.objects.usage_for_model(Entry, counts=True, filters={
            'status': Entry.STATUS_OPEN})
    poptags = dictsortreversed(poptags, 'count')

    if len(poptags) < 1:
        poptags_max = 0
    else:
        poptags_max = poptags[0].count

    return {
        'popular_tags': poptags,
        'popular_tags_max': poptags_max,
    }
