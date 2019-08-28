from enum import Enum, unique


@unique
class ShareStatus(Enum):
    private = 1
    shared = 2
    all = 3


@unique
class ArticleOperaEnum(Enum):
    get_articles = 100
    get_article_detail = 101
    get_all_articles = 102
    get_article_content = 103
    get_article_html_content = 104
    create_article = 200
    alter_article_category = 201
    update_article_content = 202
    alter_article_share_status = 203
    delete_article = 300



