var _page = 1; //当且页数
var is_end = false;
var loading = false;

$(function () {
    //隐藏标签
    $('.end').hide();
    $('.more').hide();

    //加载板块数据
    $.ajax({
        url: '/v1/category',
        type: 'GET',
        success: function (data) {
            fill_category(data);
        },
        error: function () {
            console.log('error');
        },
    });

    $(document).scroll(function () {
        var scroH = $(document).scrollTop();  //滚动高度
        var header_height = $('header').height();
        var scrollBottomHeight = -(scroH - ($(document).height() - $(window).height()));
        if(scroH > header_height){
            $('.outer').addClass('roll');
        }
        else if(scroH < header_height && $('.outer').hasClass('roll'))
        {
            $('.outer').removeClass('roll');
        };
        if(scrollBottomHeight < $('footer').height() && is_end == false && loading == false) {
            get_articles(_page+1, get_param('category_id'));
        };
    });

    //流程
    //获取文章
    get_articles(_page, get_param('category_id'));
    //隐藏上一页按钮
    $('#per_page').hide();


});

//获取url参数
function get_param(name) {
        var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if(r!=null)return  unescape(r[2]); return "";
}

//加载文章
function load_article(data){
        var strs = '';
        for(var i=0;i<data.articles.length; i++){
            var item = data.articles[i]
            strs += '<div class="post-preview">\n' +
                '<a href="/article/detail/'+ item.id +'" target="_blank">\n' +
                '<h2 class="post-title">\n' +
                item.title +
                '</h2>\n' +
                '<h3 class="post-subtitle">\n' +
                '</h3>\n' +
                '</a>\n' +
                '<p class="post-meta">\n' +
                '<i class="fas fa-book-open fa-sm">'+ item.category_name +'</i>\n' +
                '<i class="fas fa-eye fa-sm">'+ item.page_views +'</i>\n' +
                '<i class="fas fa-calendar fa-sm">'+ item.update_time +'</i>\n' +
                '</p>\n' +
                '</div>'
            };
        $('#article-items').append(strs);
    }

//获取文章
function get_articles(page, category_id) {
    loading = true;
    $('.more').show();
    $.ajax({
        url: "/v1/article",
        type: "GET",
        data: {"page": page, "num": 5,"category_id": category_id},
        success: function (data) {
            //加载文章
            load_article(data);
            $('.more').hide();
            _page = page;
            loading = false;
        },
        error: function () {
            is_end = true;
            $(".end").show();
            $('.more').hide();
        }
    })
}

//获取版块 get_category()
function fill_category(data) {
    var content = "";
    for(var key in data) {
        content += '<p>\n' +
                '<a href="/article?category_id='+ data[key].id +'">' + data[key].name + '</a>\n' +
                '</p>';
    };
    $('.outer > .content').append(content);
}
