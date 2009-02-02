import urlparse
from django.utils.safestring import mark_safe
from django import template


register = template.Library()

@register.filter
def shorten_url(url):
    return urlparse.urlsplit(url)[1]

@register.filter
def truncurl(url, chars):
    a = url.find("//")+2
    b = a + int(chars)
    if len(url) > a+b:
        return mark_safe("%s&hellip;" % url[a:b])
    return url[a:]