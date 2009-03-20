from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from tagging.models import Tag, TaggedItem
from tagging.fields import TagField
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel

class EntryManager(models.Manager):
    def public(self):
        """Returns published entries only"""
        return self.filter(status=Entry.STATUS_OPEN)
    
class Entry(TimeStampedModel):

    STATUS_CLOSED = 1
    STATUS_DRAFT = 2
    STATUS_OPEN = 3

    STATUS_CHOICES = (
        (STATUS_CLOSED, _('closed')),
        (STATUS_DRAFT, _('draft')),
        (STATUS_OPEN, _('published')),
    )
    objects = EntryManager()

    # Title and Slug
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title', max_length=255)
    content = models.TextField(_('content'))
    content_more = models.TextField(_('more content'), blank=True)
    status = models.SmallIntegerField('status', choices=STATUS_CHOICES, default=STATUS_OPEN)
    tags = TagField()
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        ordering = ('-created',)
        get_latest_by = 'created'
        permissions = (
            ('can_change_foreign', _('can change foreign entry')),
            ('can_publish', _('can publish entry')),
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
        return self.get_next_by_created(status=self.STATUS_OPEN)

    def get_prev(self):
        return self.get_previous_by_created(status=self.STATUS_OPEN)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('ticker_details', (), dict(slug=self.slug))
    get_absolute_url = permalink(get_absolute_url)

class EntryResourceType(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title', max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __unicode__(self):
        return self.title

class EntryResource(models.Model):
    entry = models.ForeignKey(Entry, verbose_name=_('entry'), related_name='resources')
    type = models.ForeignKey(EntryResourceType, verbose_name=_('resource type'))
    title = models.CharField(_('title'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    url = models.URLField(_('URL'), blank=True, verify_exists=False)

    class Meta:
        verbose_name = _('resource')
        verbose_name_plural = _('resources')

    def __unicode__(self):
        return self.title
