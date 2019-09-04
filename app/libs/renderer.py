from mistune import Renderer as _Renderer, escape
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


class TocMixin(object):
    """
        自动生成目录
    """
    def reset_toc(self):
        self.toc_tree = []
        self.toc_count = 0

    def header(self, text, level, raw=None):
        rv = '<h%d id="toc-%d">%s</h%d>\n' % (
            level, self.toc_count, text, level
        )
        self.toc_tree.append((self.toc_count, text, level, raw))
        self.toc_count += 1
        return rv

    def render_toc(self, level=3):
        """Render TOC to HTML.
        :param level: render toc to the given level
        """
        return ''.join(self._iter_toc(level))

    def _iter_toc(self, level):
        first_level = 0
        last_level = 0

        yield '<div class="toc">\n<ul>\n'

        for toc in self.toc_tree:
            index, text, l, raw = toc

            if l > level:
                # ignore this level
                continue

            if first_level == 0:
                # based on first level
                first_level = l
                last_level = l
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level == l:
                yield '</li>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level == l - 1:
                last_level = l
                yield '\n<ul>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level > l:
                # close indention
                yield '</li>'
                while last_level > l:
                    yield '\n</ul>\n</li>\n'
                    last_level -= 1
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)

        # close tags
        yield '</li>\n'
        while last_level > first_level:
            yield '</ul>\n</li>\n'
            last_level -= 1

        yield '</ul>\n</div>\n'


class HighlightMixin(object):
    """
        代码高亮
    """
    def block_code(self, text, lang):
        # renderer has an options
        inline_styles = self.options.get('inlinestyles', False)
        linenos = self.options.get('linenos', False)

        if not lang:
            text = text.strip()
            return u'<pre><code>%s</code></pre>\n' % escape(text)

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(
                noclasses=inline_styles, linenos=linenos
            )
            code = highlight(text, lexer, formatter)
            if linenos:
                return '<div class="highlight-wrapper">%s</div>\n' % code
            return code
        except:
            return '<pre class="%s"><code>%s</code></pre>\n' % (
                lang, escape(text)
            )


class Renderer(TocMixin, HighlightMixin, _Renderer):
    """
        自定义渲染器
    """
    def __init__(self, **kwargs):
        super(Renderer, self).__init__(**kwargs)
        self.reset_toc()
