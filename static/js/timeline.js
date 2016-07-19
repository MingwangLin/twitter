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
    t = data.tweets;
    visitor = data.visitor
    host = data.host
    tweets_template();
};

var tweets_template = function(){
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





