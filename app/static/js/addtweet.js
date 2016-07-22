var add_newtweet = function(){
  var content = $('#id-text-content').val();
  var form = {
    'content': content,
  };
  // JSON.stringify 可以把一个 object 转换为字符串
  var url = '/tweet/add';
  post(url, form, prepend_template);
}

var prepend_template = function(data){
      var t = data.tweet;
      var u = data.user
      var template = `
          <a href="/tweets/${t.id}" class="list-group-item">
            ${u.username} · ${formatted_time(t.created_time)}
            <br>
            ${t.content}
            <a href="/tweet/update/${t.id}">编辑</a>
            <a href="/tweet/delete/${t.id}">删除</a>
            <a href="/tweets/${t.id}">评论</a>
            <a href="/tweets/${t.id}">转发</a>
          <hr />
          </a>
          `;
        $('#id-div-tweets').prepend(template);
}