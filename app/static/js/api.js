// log
var log = function () {
    console.log(arguments);
};

// form


var ajax = function(url, method, form, response) {
    var request = {
        url: url,
        type: method,
        contentType: 'application/json',
        success: function (r) {
            log('success', url, r);
            response(r);
        },
        error: function (err) {
            r = {
                success: false,
                message: '服务器提了一个问题',
                data: err
            }
            log('err', err)
            log('err', url, err);
            response(r);
        }
    };
    if(method === 'post') {
        var data = JSON.stringify(form);
        request.data = data;
    }
    $.ajax(request);
};

var get = function(url, response) {
    var method = 'get';
    var form = {}
    ajax(url, method, form, response);
};

var post = function(url, form, response) {
    var method = 'post';
    ajax(url, method, form, response);
};

var formatted_time = function(timestamp){
  // multiplied by 1000 so that the argument is in milliseconds, not seconds
  var a = new Date(timestamp*1000);
  var now = new Date().getTime()
  var now = Math.floor(now/1000);
  var interval = now - timestamp;
  if (interval == 0) {
    var time = `现在`
  }else if (interval < 60) {
    var time = `${interval}秒前`
  }else if (interval >= 60 && interval < 3600) {
    var time = `${Math.floor(interval/60)}分钟前`
  }else if (interval >= 3600 && interval < 3600*24) {
    var time = `${Math.floor(interval/3600)}小时前`
  }else if (interval >= 3600*24 && interval < 3600*24*7) {
    var time = `${Math.floor(interval/(3600*24))}天前`
  }else{
    var year = a.getFullYear();
    var month = a.getMonth();
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    if (min < 10) {
      min = '0' + min
    }
    var time = year + '/' + month + '/' + date + ' ' + hour + ':' + min;
  }
  return time;
  }

var href_for_personalpage = function(name){
    // multiplied by 1000 so that the argument is in milliseconds, not seconds
    template = `<a class=“font-small" href="/timeline/${name}">${name}</a>`;
    return template;
    }

// API products
var products = function(response) {
    var api = this;
    var path = '/api/products';
    get(path, response);
};

var product_delete = function(product_id, response) {
    var path = '/api/products/delete/' + product_id;
    get(path, response);
};
// API articles
var articles = function(response) {
    var path = '/api/articles';
    get(path, response);
};

var href_for_username = function(content){
  while (i < 10) {
    text += "The number is " + i;
    i++;
}
  var i = content.indexof("@")
  var j = content.indexof(":")
  template = `<a href="/timeline/${username}">${username}</a>`
  return template
}
