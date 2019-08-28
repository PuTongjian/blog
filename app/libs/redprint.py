"""
    RedPrint Class
    定义红图类，用于模块级别的管理
"""


class RedPrint:
    def __init__(self, name: str, url_prefix: str = None):
        self.name = name
        self.mound = []
        self.url_prefix = url_prefix
        if not self.url_prefix:
            self.url_prefix = '/' + self.name

    def register(self, blueprint, url_prefix: str = None):
        if url_prefix:
            self.url_prefix = url_prefix

        for rule, f, options in self.mound:
            endpoint = options.pop('endpoint', f.__name__)
            blueprint.add_url_rule(self.url_prefix + rule, endpoint, f, **options)

    def route(self, rule: str, **options):
        def decorator(f: object):
            self.mound.append((rule, f, options))
            return f

        return decorator
