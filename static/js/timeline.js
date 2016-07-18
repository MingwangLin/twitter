var offset = 0;
var limit = 20;
$(document).ready(function(){
        var button = $('#id-text-submit');
        button.on('click', addtweets)
        username = $('#id-button-loadtweets').attr('data-name');
        ajax();
        $("#id-button-loadtweets").on('click', ajax)
});

var ajax = function(){
  var url = `/tweets/json/${username}?offset=${offset}&limit=${limit}`
  console.log('url', url);
  var request = {
      url: url,
      type: 'get',
      contentType: 'application/json',
      success: success
    }
  $.ajax(request);
};


var success = function(data){
    offset += limit;
    console.log('success', data);
    t = data.tweets;
    visitor = data.visitor
    host = data.host
    append_template();
};


var append_template = function(){
    if (visitor.id === host.id) {
        for(var i = 0; i < t.length; i++){
            var template = `
                <p>
                    ${t[i].content} --${formatted_time(t[i].created_time)}
                    <br>
                    <a href="/tweet/update/${t.id}">编辑</a>
                    <a href="/tweet/delete/${t.id}">删除</a>
                    <a href="/tweets/${t[i].id}">评论</a>
                    <a href="/tweets/${t[i].id}">转发</a>
                    <hr />
                </p>
                `;
                $('#id-div-tweets').append(template)

            }
        } else {
            for(var i = 0; i < t.length; i++){
                var template = `
                    <p>
                        ${t[i].content} --${formatted_time(t[i].created_time)}
                        <br>
                        <a href="/tweets/${t[i].id}">评论</a>
                        <a href="/tweets/${t[i].id}">转发</a>
                        <hr />
                    </p>
                    `;
                $('#id-div-tweets').append(template)
                }
                }
}


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

