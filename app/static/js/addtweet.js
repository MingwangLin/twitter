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
      var t = data.tweet;
      var u = data.user
      var template = `
          <a href="/tweet/${t.id}" class="list-group-item">
            ${u.username} · ${formatted_time(t.created_time)}
            <br>
            ${t.content}
            <a href="/tweet/update/${t.id}">编辑</a>
            <a href="/tweet/delete/${t.id}">删除</a>
            <a href="/tweet/${t.id}">评论</a>
            <a href="/tweet/${t.id}">转发</a>
          <hr />
          </a>
          `;
        log('template', template)
        $('#id-div-mytweets').prepend(template);
}
