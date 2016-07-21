var offset = 0;
var limit = 20;

$(document).ready(function(){
        var button = $('#id-text-submit');
        button.on('click', add_newtweet)
        username = $('#id-button-loadtweets').attr('data-name');

        var url = `/tweets/json/${username}?offset=${offset}&limit=${limit}`
        log('url', url)
        show_tweets(url, tweets_response);
        $("#id-button-loadtweets").on('click', function(){
          show_tweets(url, tweets_response)
        })
});

var show_tweets = function(url,response){
  get(url, response);
}

var tweets_response = function(data){
    offset += limit;
    log('success', data);
    var t = data.tweets;
    var host = data.host
    visitor = data.visitor
    tweets_template(t, host);
};

var tweets_template = function(tweets, host){
    var t = tweets
    if (visitor.id === host.id) {
        for(var i = 0; i < t.length; i++){
            var template = `
                <a href="/tweets/${t[i].id}" class="list-group-item">
                  ${host.username} · ${formatted_time(t[i].created_time)}
                  <br>
                  ${t[i].content}
                  <a href="/tweet/update/${t[i].id}">编辑</a>
                  <a href="/tweet/delete/${t[i].id}">删除</a>
                  <a href="/tweets/${t[i].id}">评论</a>
                  <a href="/tweets/${t[i].id}">转发</a>
                <hr />
                </a>
                `;
                $('#id-div-tweets').append(template)

            }
        } else {
            for(var i = 0; i < t.length; i++){
                var template = `
                      <a href="/tweets/${t[i].id}" class="list-group-item">
                        ${host.username} · ${formatted_time(t[i].created_time)}
                        <br>
                        ${t[i].content}
                        <a href="/tweets/${t[i].id}">评论</a>
                        <a href="/tweets/${t[i].id}">转发</a>
                      <hr />
                      </a>
                    `;
                $('#id-div-tweets').append(template)
                }
                }
}
