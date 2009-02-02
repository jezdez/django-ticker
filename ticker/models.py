import datetime
from django.db import models
from django.db.models import Q
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from tagging.models import Tag, TaggedItem
from tagging.fields import TagField
from django_extensions.db.fields import AutoSlugField

from ticker import textutils

class EntryManager(models.Manager):
    def public(self):
        return self.filter(status=Entry.STATUS_OPEN)

class Entry(models.Model):

    STATUS_CLOSED = 1
    STATUS_DRAFT = 2
    STATUS_OPEN = 3

    STATUS_CHOICES = (
        (STATUS_CLOSED, _('Closed')),
        (STATUS_DRAFT, _('Draft')),
        (STATUS_OPEN, _('Open')),
    )
    objects = EntryManager()

    # Title and Slug
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title', max_length=255, blank=True)

    content = models.TextField(_('content'))
    content_processed = models.TextField(_('content (parsed)'), blank=True)
    source_url = models.URLField(_('source URL'),blank=True)

    # Date Fields
    published = models.DateTimeField(_('published'))
    modified = models.DateTimeField(_('modified'))

    # Status Fields
    status = models.SmallIntegerField('Status',
        choices=STATUS_CHOICES, default=STATUS_OPEN)

    # Related
    tags = TagField()
    author = models.ForeignKey(User)

    enable_comments = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        ordering = ('-published',)
        permissions = (
            ('can_change_foreign', _('Can change foreign entry')),
            ('can_publish', _('Publish instantly')),
        )

    def get_author(self):
        name = self.author.get_full_name()
        if name:
            return name
        return self.author.username

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_related(self):
        return TaggedItem.objects.get_related(self, Entry.objects.public())

    def get_related_tags(self):
        return Tag.objects.related_for_model(self.tags, Entry)

    def get_next(self):
        return self.get_next_by_published(status=self.STATUS_OPEN)

    def get_prev(self):
        return self.get_previous_by_published(status=self.STATUS_OPEN)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.published = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        self.content_processed = textutils.textfilter(self.content)
        super(Entry, self).save(force_insert, force_update)

    def get_absolute_url(self):
        return ('ticker_details', (), dict(slug=self.slug))
    get_absolute_url = permalink(get_absolute_url)
