import pygments
import pygments.lexers as lexers
import pygments.formatters as formatters
from pygments.util import ClassNotFound

from markdown import markdown
from md5 import md5
from random import random
import re

def uniqid(chars=5):
    """Generates a unique id like 'cfce2' or '76e03'"""
    return md5(str(random())).hexdigest()[:chars]

def unescape_amp(text):
    return text.replace('&amp;', '&')

class NakedHtmlFormatter(formatters.HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)
    def _wrap_code(self, source):
        for i, t in source:
            yield i, t

class CodeHtmlFormatter(formatters.HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)
    def _wrap_code(self, source):
        uniq = uniqid()
        yield 0, '<pre class="highlight" id="codeblock_%s"><code>' % uniq
        for i, t in source:
            #if i == 1:
                # it's a line of formatted code
                #t += '<br/>'
            yield i, t
        yield 0, '</code></pre>'

def get_lexer(code_string):
    '''
    Extract lexer name by the first line of the codeblock.

    You can specify the lexer name in the  first line of your code block.
    See example for further details. If no lexer is found or can not be guessed,
    the default lexer is ``text``.

    See AvailableLexers_ for available lexers.

    .. _AvailableLexers: http://pygments.org/docs/lexers/

    Lexer Line::

        #$type: <lexername>

    Example Code::

        #$type: python
        def my_python_function(foo):
            return foo
    '''
    lexer_line = code_string.splitlines()[0]
    if lexer_line.startswith('#$type: '):
        lexer_name = lexer_line.split()[1].strip(' ')
        code_string = '\n'.join(code_string.splitlines()[1:])
        try:
            lexer = lexers.get_lexer_by_name(lexer_name)
        except ClassNotFound:
            try:
                lexer = lexers.guess_lexer(code_string)
            except ClassNotFound:
                lexer = lexers.get_lexer_by_name('text')
    else:
        try:
            lexer = lexers.guess_lexer(code_string)
        except ClassNotFound:
            lexer = lexers.get_lexer_by_name('text')
    return (code_string, lexer)

def pygmentize(value):
    regex = re.compile(r'(<pre><code>(.*?)</code></pre>)', re.DOTALL)
    last_end = 0
    to_return = ''
    found = 0
    for match_obj in regex.finditer(value):
        code_string = match_obj.group(2)
        code_string, lexer = get_lexer(code_string)
        pygmented_string = pygments.highlight(code_string, lexer, CodeHtmlFormatter())
        pygmented_string = unescape_amp(pygmented_string)
        to_return = to_return + value[last_end:match_obj.start(1)] + pygmented_string
        last_end = match_obj.end(1)
        found += 1
    to_return = to_return + value[last_end:]
    return to_return

def textfilter(text):
    text = markdown(text)
    text = pygmentize(text)
    return text
