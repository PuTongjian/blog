import time
from markdown import Markdown

from app.libs.enums import ArticleOperaEnum


parameters = {
    ArticleOperaEnum.create_article.name: ['id', 'title', 'category_id', 'sharing_status'],
    ArticleOperaEnum.get_articles.name: ['id', 'title', 'category_name', 'update_time', 'page_views'],
    ArticleOperaEnum.get_all_articles.name: ['id', 'title', 'category_id', 'sharing_status'],
    ArticleOperaEnum.get_article_detail.name: ['id', 'title', 'html_content'],
    ArticleOperaEnum.get_article_content.name: ['content'],
    ArticleOperaEnum.get_article_html_content.name: ['html_content']
}


class ArticleViewModel:
    def __init__(self, model: dict, opera_code: int):
        if not isinstance(model, dict):
            model = dict(model)
        self.id = model['id']
        self.title = model['title']
        self._update_time = model['update_time']
        self.page_views = model['page_views']
        self.content = model['content']
        self.sharing_status = model['sharing_status']

        category = dict(model['category']) if model['category'] else None
        self.category = category

        name = ArticleOperaEnum(opera_code).name
        self.field = parameters[name]

    @property
    def update_time(self):
        time_array = time.localtime(self._update_time)
        return time.strftime('%Y %m %d', time_array)

    @property
    def category_id(self):
        return self.category['id']

    @property
    def category_name(self):
        return self.category['name']

    @property
    def html_content(self):
        md = Markdown(
            extensions=[
                # 包含 缩写、表格等常用扩展
                'markdown.extensions.extra',
                # 语法高亮扩展
                'markdown.extensions.codehilite',
                # 允许我们自动生成目录
                'markdown.extensions.toc'
            ])
        _html_content = md.convert(self.content)

        return _html_content

    def keys(self):
        return self.field

    def __getitem__(self, item):
        return getattr(self, item, None)


class ArticleViewModelCollection:
    def __init__(self):
        self.total = 0
        self.articles = []

    def fill(self, articles: list, opera_code: int):
        self.total = articles.__len__()

        self.articles = [ArticleViewModel(dict(article), opera_code)for article in articles]

    @property
    def first(self):
        return self.articles[0] if self.total > 0 else None

    def keys(self):
        return ['total', 'articles']

    def __getitem__(self, item):
        return getattr(self, item, None)

