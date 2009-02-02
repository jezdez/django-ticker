from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from threadedcomments.forms import FreeThreadedCommentForm

class BetterFreeThreadedCommentForm(FreeThreadedCommentForm):

    def __init__(self, *args, **kwargs):
        super(BetterFreeThreadedCommentForm, self).__init__(*args, **kwargs)

        # Hide fields
        self.fields['markup'].widget = forms.HiddenInput()
        self.fields['email'].widget = forms.HiddenInput(attrs={'autocomplete': 'off'})

    def clean_email(self):
        """
        A HiddenInput as a honeypot.
        Returns a error message if a e-mail address was entered.
        """
        if self.cleaned_data.get('email', False):
            raise forms.ValidationError("We DON'T want to know your e-mail " \
                "address, please leave this field empty.")
        return self.cleaned_data.get('email')

    def clean_name(self):
        '''
        Simples Keyword-Blocking. Gesperrte Usernamen werden in einer Tupel in
        settings.THREADEDCOMMENTS_BLOCKED_USERNAMES definiert.
        '''
        this_name = self.cleaned_data.get('name')
        for blocked_name in getattr(settings, 'THREADEDCOMMENTS_BLOCKED_USERNAMES', ()):
            if blocked_name in this_name:
                raise forms.ValidationError(_('Your name contains a blocked '
                    'word: "%s" Please remove it from your name.' % blocked_name))
        return this_name
