var addtweets = function(){
  var content = $('#id-text-content').val();
  var tweet = {
    'content': content,
  };
  // JSON.stringify 可以把一个 object 转换为字符串
  var postData = JSON.stringify(tweet);
  var request = {
    url: '/tweet/add',
    type: 'post',
    contentType: 'application/json',
    data: postData,
    success: function(data){
      var t = data;
      console.log('t', t)
      var template = `
          <p>
          ${t.content} --${formatted_time(t.created_time)}
          <br>
          <a href="/tweet/update/${t.id}">编辑</a>
          <a href="/tweet/delete/${t.id}">删除</a>
          <a href="/tweets/${t.id}">评论</a>
          <a href="/tweets/${t.id}">转发</a>
          <hr />
          </p>
          `;
        $('#id-div-tweets').prepend(template);

      }
  };
  $.ajax(request);
}
