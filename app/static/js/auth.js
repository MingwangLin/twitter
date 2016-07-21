$(document).ready(function(){
            console.log('ready');
            var login_button = $('#id-button-submit');
            var register_button = $('#id-button-newusr-submit');
            login_button.on('click', login_submit)
            register_button.on('click', register_submit)
            $('#id-text-password').on('keypress', function(e) {
              if(e.which == 13) {
                 login_submit()               }
         });
            $('#id-text-newusr-password').on('keypress', function(e) {
              if(e.which == 13) {
                register_submit()               }
            });
         });

var login_submit = function(){
  log('click button');
  var username = $('#id-text-username').val();
  var password = $('#id-text-password').val();
  log('user', username, password);
  var form = {
    'username': username,
    'password': password
  };
    url = '/login'
    post(url, form, auth_response)
  }

var register_submit = function(){
  var username = $('#id-text-newusr-username').val();
  var password = $('#id-text-newusr-password').val();
  log('user', username, password);
  var form = {
    'username': username,
    'password': password
  };
  // JSON.stringify 可以把一个 object 转换为字符串
  url = '/register'
  post(url, form, auth_response)
}

var auth_response = function(r){
  log('response', r);
  if(r.success) {
    log('成功');
    var url = r.data;
    window.location.href = url;
  } else {
    log('失败');
  }
  $('#id-p-info').text(r.message);
}
