var _articles = {};
var _article_contents = {};
var start = false;
var save_enable = true;
var isSaved = false;
var save_timer = null;

//私密文章和已发布文章的样式
var sharing_style = {
    1 : '',
    2 : 'color: #51cf66'
};
//私密文章和已发布文章的选择器
var sharing_class = {
    1 : 'private',
    2 : 'shared'
};

$(function () {
    //全局变量
    //初始化页面
    init();
});

//页面初始化函数
function init() {
    //为控件绑定事件
    //监听 添加版块按钮
    $('.add-category > .add-button').on('click', function () {
       var add_btn = $('.add-category-info > .hidden');
       add_btn.removeClass();
       add_btn.addClass('show');
    });

    //监听 添加文章按钮
    $('.add-article > .add-button').on('click', function () {
        var category_id = $('#category > .item-selected').attr('data-id');
        var data = new Date();
        var title = data.getFullYear()+"-"+(data.getMonth()+1)+"-"+data.getDate();
        create_article(title, category_id);

    });

    //监听 取消添加版块按钮
    $('button.btn-cancel').on('click', function () {
       var add_btn = $('.add-category-info > .show');
       add_btn.removeClass();
       add_btn.addClass('hidden');
       //清空input中的值
       $('input.category-name').val('');
    });

    //监听 模块创建按钮
    $('button.btn-submit').on('click', function () {
       var category_name = $('input.category-name');
       var val = category_name.val();
       if(val.length >= 1){
           create_category(val);
           var add_btn = $('.add-category-info > .show');
           add_btn.removeClass();
           add_btn.addClass('hidden');
           //清空input中的值
           category_name.val('');
       }
       else{
            BootstrapDialog.show({
                title: '提示',
                message: '板块名称不能为空'
            });
       };
    });

    //监听保存文章按钮
    $('a[data-action=save]').on('click', function () {
        var select_article = $('#article > .item-selected');
        var title = $('.title-input').val();
        var content = $('#arthur-editor').val();
        if(title.length < 1){
            $('.title-input').attr('placeholder', '文章名称不能为空');
        }
        else if(select_article.length > 0 && save_enable){
            save_article_content(select_article.attr('data-id'), title, content);
            if(isSaved){
                save_enable = false;
                $(this).removeClass('fa-save');
                $(this).addClass('fa-check-circle');
                setTimeout(function () {
                    $('a[data-action=save]').removeClass('fa-check-circle');
                    $('a[data-action=save]').addClass('fa-save');
                    save_enable = true;
                    isSaved = false;
                }, 2000)
            };
        };
    });

    //监听发布按钮
    $('a[data-action=compile]').on('click', function () {
        $('a[data-action=save]').trigger('click');
        var msg = "文章已经发布";
        if (isSaved) {
            alter_sharing_status(2);
        } else {
            msg = "发布失败，请稍后重试";
        };
        BootstrapDialog.show({
            message: msg,
            onshown: function (dialog) {
                setTimeout(function () {
                    dialog.close();
                }, 1000)
            },
        });
    });

    //监听预览按钮
    $('a[data-action=to-preview]').on('click', function () {
        if($(this).hasClass('preview')){
            $('.markdown-editor').removeClass('hidden');
            $('.markdown-preview').text('').addClass('hidden');
            $(this).removeClass('preview');
        }
        else {
            var article_id = $('#article > .item-selected').attr('data-id');
            var content = $('.markdown-editor').val();
            get_article_html_content(article_id, content);
            $('.markdown-editor').addClass('hidden');
            $('.markdown-preview').append(_article_contents[article_id].html_content).removeClass('hidden');
            $(this).addClass('preview');
        };
    });

    //监听编辑器输入事件
    $('.markdown-editor').bind('input propertychange', function(){
        if(!start) {
            start = true;
            var id = $('#article > .item-selected').attr('data-id');
            save_timer = setTimeout(function () {
                var current_id = $('#article > .item-selected').attr('data-id');
                if(id == current_id){
                    $('a[data-action=save]').trigger('click');
                    start = false;
                    save_timer = null;
                }
            }, 1000 * 60 * 2);
        };
    });

    document.addEventListener('dragover', function(e) {
        e.stopPropagation();
        e.preventDefault();
    }, false);

    document.addEventListener('drop', function(e) {
        e.stopPropagation();
        e.preventDefault();
    }, false);

    $('.markdown-editor').on('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();
        var dt = e.originalEvent.dataTransfer;
        var reader = new FileReader();
        reader.readAsDataURL(dt.files[0]);
        reader.onload = function(){
            $.ajax({
                url: '/v1/article/upload_images',
                type: 'POST',
                processData : false, 	//必须false才会自动加上正确的Content-Type
				contentType : false,
                data: this.result,
                success: function (data) {
                    var image_name = dt.files[0].name;
                    var url = data.image_url + '/480';
                    var image = '!['+ image_name +']('+ url +')';
                    $('.markdown-editor').val($('.markdown-editor').val() + '\n' + image);
                },
                error: function () {
                }
            });
        };
    });

    //监听ctrl + s 事件
    $(document).unbind('keydown').bind('keydown', function(e){
        if(e.ctrlKey && e.keyCode  == 83) {
            $('a[data-action=save]').trigger('click');
            // 返回false, 防止重复触发copy事件
            return false;
        }
        else if(e.keyCode == 9) {
            return false;
        };
    });

    //加载板块数据
    $.ajax({
        url: '/v1/category',
        type: 'GET',
        success: function (data) {
            for(var i = 0; i < data.length; i++){
                _articles[data[i].id] = null;
            }
            fill_category(data);
        },
        error: function () {
            console.log('error');
        },
    })
}

//加载category内容
function fill_category(data) {
    var body = '';
    for(var i = 0; i < data.length; i++){
         body += '<li  class="item category-item" data-id="'+ data[i].id +'">\n' +
                 '<div class="item-edit-btn category-settings btn-group"><i class="fa fa-cog fa-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
                 '<ul class="dropdown-menu">\n' +
                 '<li><a href="javascript:void(0);" onclick="rename_category()">更改名称</a></li>\n' +
                 '<li><a href="javascript:void(0);" onclick="delete_category()">删除版块</a></li>\n' +
                 '</ul></i></div>'+
                 '<span>'+ data[i].name +'</span>\n' +
                 '</li>';
    };
    $('#category').prepend(body);
    $('.category-settings').hide();
    $('.category-item').on('click', function () {
        if(!$(this).is($('#category > .item-selected'))){
            $('.title-input').val('');
            $('.markdown-editor').val('');
            $('.col-md-7').hide();


            $('.category-settings').hide();
            $('.category-item').removeClass('item-selected');
            $(this).children('.category-settings').show();
            $(this).addClass('item-selected');

            $('#article').children().remove();
            get_all_articles($(this).attr('data-id'));
        }
    });
    //加载完成后选中第一个元素
    $('ul#category > li:first').trigger('click');
}

//重命名版块名称
function rename_category() {
        BootstrapDialog.show({
            title: '更改名称',
            message: '<input type="text" class="category-name" placeholder="请输入板块名..." maxlength="20">',
            buttons: [{
                label: '取消',
                cssClass: 'sm-btn btn-cancel',
                action: function(dialogRef) {
                    dialogRef.close();
                }
            },
            {
                label: '确认',
                cssClass: 'sm-btn btn-submit',
                action: function(dialogRef) {
                    var input = dialogRef.getModalBody().find('input');
                    var name = input.val();
                    var select_category = $('#category > .item-selected')
                    if(name.length > 0){
                        $.ajax({
                            url: '/v1/category/name',
                            type: 'POST',
                            dataType: 'json',
                            headers: {'Content-Type': 'application/json'},
                            data: JSON.stringify({'id': select_category.attr('data-id'), 'name': name}),
                            success: function (data) {
                                select_category.children('span').text(name);
                                dialogRef.close();
                            },
                            error: function () {
                                input.val('');
                                input.attr('placeholder', '操作失败');
                            }
                        })
                    }
                    else {
                        input.attr('placeholder', '请输入版块名称');
                    };
                }
            }]
    });
}

//删除某一版块
function delete_category() {
    BootstrapDialog.show({
        message: '确定要删除版块',
        title: '确认删除',
        buttons: [{
            label: '取消',
            cssClass: 'sm-btn btn-cancel',
            action: function(dialogRef) {
                dialogRef.close();
            }
        },
        {
            label: '确认',
            cssClass: 'sm-btn btn-submit',
            action: function(dialogRef) {
                var select_category = $('#category > .item-selected');

                $.ajax({
                    url: '/v1/category',
                    type: 'DELETE',
                    dataType: 'json',
                    headers: {'Content-Type': 'application/json'},
                    data: JSON.stringify({'id': select_category.attr('data-id')}),
                    success: function (data) {
                        delete _articles[select_category.attr('data-id')];
                        select_category.remove();
                        $('ul#category > li:first').trigger('click');
                        dialogRef.close();
                    },
                    error: function () {
                        dialogRef.setMessage('操作失败，是否继续？')
                    }
                })
            }
        }]
    });
}

//创建新的版块
function create_category(name) {
    $.ajax({
        url: '/v1/category',
        type: 'POST',
        dataType: 'json',
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({'name': name}),
        success: function (data) {
            _articles[data.id] = null;
            fill_category([data])
        },
        error: function () {
            console.log('error');
        }
    })
}

//获取某一版块所有文章
function get_all_articles(category_id) {
    var articles = _articles[category_id];
    if(articles == null){
            $.ajax({
            url: '/v1/article/all',
            type: 'GET',
            data: {'category_id': category_id},
            success: function (data) {
                _articles[category_id] = {};
                for(var i in data.articles){
                    var id = data.articles[i].id;
                    _articles[category_id][id] = {
                        'title': data.articles[i].title,
                        'sharing_status': data.articles[i].sharing_status
                    };
                    _article_contents[id] = {
                    'raw_content': null,
                    'html_content': null
                    };
                }
                fill_article(_articles[category_id]);

            },
            error: function () {
                console.log('error');
            }
        })
    }
    else{
        fill_article(articles)
    };
}

//加载文章列表
function fill_article(data) {
    var body = '';

    for(var key in data){
        var sharing_status = data[key].sharing_status
        var color = sharing_style[sharing_status]
        body += '<li  class="item-lg item article-item" data-id="'+ key +'" data-title='+ data[key].title +'>\n' +
             '<div class="item-edit-btn article-settings btn-group"><i class="fa fa-cog fa-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
             '<ul class="dropdown-menu">\n' +
             '<li class="'+ sharing_class[sharing_status] +'" data-title="private-btn"><a data-action="set-article-private">设为私密</a></li>\n' +
             '<li><a data-action="delete-article">删除文章</a></li>\n' +
             '</ul></i></div>'+
             '<span><i class="far fa-sticky-note fa-lg" style="'+ color +'">&nbsp;</i>' +
             '<i class="title">'+ data[key].title +'</i></span>\n' +
             '</li>';
    }
    $('#article').prepend(body);
    $('.article-settings').hide();
    $('.article-item').on('click', function () {
        if(!$(this).is($('#article > .item-selected'))) {
            $('.col-md-7').show();
            if(save_timer){
                clearTimeout(save_timer);
                save_timer = null;
                start = false;
                $('a[data-action=save]').trigger('click');
            };

            if($('a[data-action=to-preview]').hasClass('preview')){
                $('.markdown-editor').removeClass('hidden');
                $('.markdown-preview').text('').addClass('hidden');
                $('a[data-action=to-preview]').removeClass('preview');
            };

            $('.article-settings').hide();
            $('.article-item').removeClass('item-selected');
            $(this).children('.article-settings').show();
            $(this).addClass('item-selected');
            $('.title-input').val($(this).attr('data-title'));

            get_article_content($(this).attr('data-id'));
        }
    });

    $('a[data-action=delete-article]').on('click', function () {
        delete_article();
    });

    $('a[data-action=set-article-private]').on('click', function () {
        alter_sharing_status(1)
    });

    $('ul#article > li:first').trigger('click');
}

//删除某一文章
function delete_article() {
    var select_article = $('#article > .item-selected');
    BootstrapDialog.show({
        message: '确定要删除《'+ select_article.attr('data-title') +'》文章',
        title: '确认删除',
        buttons: [{
            label: '取消',
            cssClass: 'sm-btn btn-cancel',
            action: function(dialogRef) {
                dialogRef.close();
            }
        },
        {
            label: '确认',
            cssClass: 'sm-btn btn-submit',
            action: function(dialogRef) {
                var article_id = select_article.attr('data-id');
                $.ajax({
                    url: '/v1/article',
                    type: 'DELETE',
                    dataType: 'json',
                    headers: {'Content-Type': 'application/json'},
                    data: JSON.stringify({'id': article_id}),
                    success: function (data) {
                        select_article.remove();
                        if($('ul#article > li:first').length > 0) {
                            $('ul#article > li:first').trigger('click');
                        }
                        else {
                            $('.col-md-7').hide();
                        }
                        dialogRef.close();

                        var category_id = $('#category > .item-selected').attr('data-id');
                        delete _articles[category_id][article_id];
                        delete _article_contents[article_id];
                    },
                    error: function () {
                        dialogRef.setMessage('操作失败，是否继续？')
                    }
                })
            }
        }]
    });
}

//更改文章分享状态
function alter_sharing_status(sharing_status) {
    var select_article = $('#article > .item-selected');
    var article_id = select_article.attr('data-id');
    var category_id = $('#category > .item-selected').attr('data-id');
    $.ajax({
            url: '/v1/article/share',
            type: 'POST',
            dataType: 'json',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({'id': article_id, 'sharing_status': sharing_status}),
            success: function (data) {
                select_article.find('.fa-sticky-note').attr('style', sharing_style[sharing_status]);
                select_article.find('li[data-title=private-btn]').attr('class', sharing_class[sharing_status]);

                _articles[category_id][article_id].sharing_status = sharing_status;
            },
            error: function () {
            }
        })
}

//创建文章
function create_article(title, category_id) {
    $.ajax({
            url: '/v1/article',
            type: 'POST',
            dataType: 'json',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({'category_id': category_id, 'title': title}),
            success: function (data) {
                var id = data.id;
                _articles[category_id][id] = {
                    'title': data.title,
                    'sharing_status': data.sharing_status
                };
                _article_contents[id] = {
                    raw_content: ' ',
                    html_content: null,
                };

                var r = {};
                r[id] = _articles[category_id][id];
                fill_article(r);
            },
            error: function () {
                BootstrapDialog.show({
                    title: '提示',
                    message: '文章创建失败'
                });
            }
    })
}

//获取文章内容
function get_article_content(article_id) {
    var content = _article_contents[article_id].raw_content;
    if(!content){
        $.ajax({
            url: '/v1/article/content',
            type: 'GET',
            data: {'id': article_id},
            success: function (data) {
                _article_contents[article_id].raw_content = data.content;
                $('#arthur-editor').val(data.content);
            },
            error: function () {
                console.log('error');
            }
        })
    }
    else{
        $('.markdown-editor').disable = false;
        $('#arthur-editor').val(content);
    };
}

//获取转译成html的文章内容
function get_article_html_content(article_id, content) {
    var html_content = _article_contents[article_id].html_content;
    var is_changed = !($('.markdown-editor').val() == _article_contents[article_id].raw_content);
    if(!html_content || is_changed) {
        $.ajax({
            url: '/v1/article/content/html',
            type: 'POST',
            dataType: 'json',
            headers: {'Content-Type': 'application/json'},
            async: false,
            data: JSON.stringify({'content': content}),
            success: function (data) {
                _article_contents[article_id].html_content = data.html_content;
            },
            error: function () {

            }
        })
    }

}

//保存文章
function save_article_content(article_id, title, content) {
    var category_id = $('#category > .item-selected').attr('data-id');
    if(!(title == _articles[category_id][article_id].title) ||
        !(content == _article_contents[article_id].raw_content )){
            $.ajax({
                url: '/v1/article/content',
                type: 'POST',
                dataType: 'json',
                headers: {'Content-Type': 'application/json'},
                async: false,
                data: JSON.stringify({'id': article_id, 'title': title, 'content': content}),
                success: function (data) {
                    _article_contents[article_id].raw_content = content;
                    _articles[category_id][article_id].title = title;
                    $('#article > .item-selected > span > i.title').text(title);
                    $('#article > .item-selected').attr('data-title', title);
                    isSaved = true;
                },
                error: function () {
                    isSaved = false;
                }
            })
    }
    else {
        isSaved = true;
    };
}

