from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext as _

from ticker.models import Entry

class LatestEntries(Feed):
    title = _("Latest news")
    link = "/"

    def items(self):
        return Entry.objects.public()[:30]

    def item_pubdate(self, item):
        return item.created

    def item_author_name(self, item):
        return item.get_author()

class LatestEntriesAtom(LatestEntries):
    feed_type = Atom1Feed

feeds = {
    'rss': LatestEntries,
    'atom': LatestEntriesAtom,
}
