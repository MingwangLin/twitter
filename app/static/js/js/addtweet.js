var add_newtweet = function(){
  var content = $('#id-text-content').val();
  var form = {
    'content': content,
  };
  // JSON.stringify 可以把一个 object 转换为字符串
  var url = '/tweet/add';
  log('content', content)
  post(url, form, prepend_template);
}

var prepend_template = function(data){
  if(data.success) {
      var t = data.tweet;
      var u = data.user
      var template = `
            <div class="well clearfix" data-id="${t.id}">
            ${u.username} · ${formatted_time(t.created_time)}
            <br>
            ${t.content}
            ${basic_template}
          </div>
          <hr />
          `;
        log('template', template)
        $('#id-div-mytweets').prepend(template);
}else {
  log('请求失败');
}
}
