# 引言
搭建该博客网站主要有三个目的，一是为检验一下近期的学习成果（其实也没啥技术含量），二是为了记录一下自己的学习历程，最后一点也是为自己搭建一个展示的平台，尝试着营销自己。

该博客网站后端使用Python3，基于Flask框架开发。前端使用Bootstrap框架设计，大部分页面采用JS渲染数据。使用Nginx、uwsgi方式部署在阿里云服务器上。该文章对博客的设计和搭建进行一个简单的描述。

# 链接
-  [项目源码](https://github.com/PuTongjian/blog)
-  [网站地址](http://47.103.198.17/index)

# 项目设计概要
- API接口遵从RESTful设计风格。
- 遵从缓存原则，使用[Flask-Caching](https://pythonhosted.org/Flask-Caching/)插件加速网站访问速度。
- 页面数据采用JS方式渲染，部分页面数据采用jinja2模板渲染（文章详细页面）。
- 使用[Flask-Login](http://www.pythondoc.com/flask-login/)插件进行登录、登出管理以及访问权限控制。
- 使用Flask_Limiter插件对访问进行限速管理。
- 支持版块和文章的管理，包括添加、删除、重命名、编辑、发布等等（必须登录后才可进行相关操作）。
- 文章支持markdown语法，并且提供相关接口，可直接把markdown转化为html文本。

#项目目录概要
~~~
|-- blog
    |-- lauch.py               # 项目启动文件
    |-- Pipfile               # pipenv命令的依赖包
    |-- app 
        |-- app.py
        |-- __init__.py
        |-- api               # 项目API接口文件
        |   |-- v1               # v1版本接口文件
        |       |-- article.py               # 文章相关的接口
        |       |-- category.py               # 版块相关的接口
        |       |-- manager.py               # 管理员接口
        |       |-- __init__.py
        |-- config               #配置文件
        |   |-- secure.py               #敏感配置文件
        |   |-- settings.py               #通用配置文件
        |-- forms               #表单验证
        |   |-- manager.py
        |   |-- __init__.py
        |-- libs               #自定义扩展
        |   |-- api_exceptions.py               #自定义API异常处理类
        |   |-- cahce.py               # 第三方插件Flask-Caching
        |   |-- enums.py               # 定义了一些枚举
        |   |-- limiter.py               # 第三方插件Flask-Limiter
        |   |-- redprint.py               # 自定义类 红图
        |-- models               # 实体类文件，用于数据库映射
        |   |-- article.py
        |   |-- base.py
        |   |-- category.py
        |   |-- manager.py
        |   |-- __init__.py
        |-- static               # 静态文件，存放css、js等文件
        |-- templates               # 模板文件
        |   |-- article.html
        |   |-- article_detail.html
        |   |-- article_editor.html
        |   |-- index.html
        |   |-- layout.html
        |   |-- login.html
        |-- validators               # API验证文件，用于验证API请求参数合法性
        |   |-- article.py
        |   |-- base.py
        |   |-- category.py
        |   |-- manager.py
        |   |-- __init__.py
        |-- views               # 视图类文件
        |   |-- article.py
        |   |-- index.py
        |   |-- manager.py
        |   |-- __init__.py
        |-- view_models               #视图模型类
        |   |-- article.py
        |   |-- __init__.py
~~~

#项目界面预览

- 主页

![index.jpg](https://s2.ax1x.com/2019/09/24/ukJRaT.png)

- 文章列表页面，数据采用瀑布式加载

![article.jpg](https://s2.ax1x.com/2019/09/24/ukJjiD.png)

- 文章编辑页面，支持文章预览

![editor.jpg](https://s2.ax1x.com/2019/09/24/ukYQe0.png)

- 文章详细页面

![detail.jpg](https://s2.ax1x.com/2019/09/24/ukYHpQ.png)

#补充
博客网站将一直不定期维护升级，该版块不会详细描述博客搭建的每一个流程，但会记录在搭建博客网站过程中一些值得记录的技术。
