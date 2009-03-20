from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from ticker.feeds import feeds
from ticker.views import overview, archive, archive_by_tag, details

urlpatterns = patterns('',
    # The overview
    url(r'^$', overview, name='ticker_overview'),
    
    # Feed of latest additions
    url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': feeds}, name='ticker_feeds'),

    # Archive site
    url(r'^archive/$', archive, name='ticker_archive'),
    
    # Archive for a specific tag
    url(r'^archive/(?P<tag>[\w\s_\-\.% ]+)/$', archive_by_tag, name='ticker_archive_for_tag'),

    # Detail page
    url(r'^(?P<slug>[-\w]+)/$', details, name='ticker_details'),
)
