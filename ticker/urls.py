from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from ticker.feeds import feeds
from ticker.views import overview, archive, archive_by_tag, details

urlpatterns = patterns('',
    url(r'^$', overview, name='ticker_overview'),
    url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': feeds}, name='ticker_feeds'),

    url(r'^archive/$', archive, name='ticker_archive'),
    url(r'^archive/(?P<tag>[\w\s_\-\.% ]+)/$', archive_by_tag, name='ticker_archive_details'),

    # Details
    url(r'^(?P<slug>[-\w]+)/$', details, name='ticker_details'),
)
