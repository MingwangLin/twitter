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
                message: '网络错误',
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
  var year = a.getFullYear();
  var month = a.getMonth();
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var time = year + '/' + month + '/' + date + ' ' + hour + ':' + min;
  return time;
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