var mytweets_offset = 0;
var mytweets_limit = 20;
var followeetweets_offset = 0;
var followeetweets_limit = 20;

$(document).ready(function(){
        username = $('#id-button-load-mytweets').attr('data-name');
        log('username', username)
        var mytweets_url = '/tweets/' + username + '?offset=' + mytweets_offset + '&limit=' + mytweets_limit
        var followeetweets_url = '/followee_tweets/' + username + '?offset=' + followeetweets_offset + '&limit=' + followeetweets_limit
        show_tweets(mytweets_url, mytweets_response);
        show_tweets(followeetweets_url, followeetweets_response)
        __main()


});

var __main = function() {
    setup();
    bindActions();
    $('#id-a-mytweets').click();

};

var setup = function() {
    $('.blog-nav> a').on('click', function () {
              var self = $(this);
              $('.active').removeClass('active');
              self.addClass('active');
          });
    var tabAction = function (show_mytweets) {
        $('#id-div-mypage').toggle(show_mytweets);
        $('#id-div-followeepage').toggle(!show_mytweets);
    };

    $('#id-a-mytweets').on('click', function() {
        var show_mytweets = true;
        tabAction(show_mytweets);
    });
    $('#id-a-followeetweets').on('click', function() {
        var show_mytweets= false;
        tabAction(show_mytweets);
    });
};

var bindActions = function() {
    $('#id-button-load-mytweets').on('click', function(){
      var mytweets_url = '/tweets/' + username + '?offset=' + mytweets_offset + '&limit=' + mytweets_limit
      show_tweets(mytweets_url, mytweets_response)
    });

    $('#id-button-load-followeetweets').on('click', function(){
        var followeetweets_url = '/followee_tweets/' + username + '?offset=' + followeetweets_offset + '&limit=' + followeetweets_limit
        show_tweets(followeetweets_url, followeetweets_response);
    });

    $('#id-button-addtweet').on('click', add_newtweet);

};




var show_tweets = function(url,response){
  get(url, response);
}

var mytweets_response = function(data){
  if(data.success) {
    mytweets_offset += mytweets_limit;
    log('success', data);
    var tweets = data.tweets;
    var host = data.host
    var visitor = data.visitor
    my_tweets_template(tweets, host, visitor);
}else {
  log('请求失败');
}
};

var followeetweets_response = function(data){
  if(data.success) {
    followeetweets_offset += followeetweets_limit;
    log('success', data);
    var followee_tweets = data.followee_tweets;
    log('followee_tweets', followee_tweets)
    var host = data.host
    var visitor = data.visitor
    followee_tweets_template(followee_tweets, host, visitor);
  }else {
    log('请求失败');
  }
};

var my_tweets_template = function(tweets, host, visitor){
    var t = tweets
    if (visitor.id === host.id) {
        for(var i = 0; i < t.length; i++){
            var template = `
                <a href="/tweet/${t[i].id}" class="list-group-item">
                  ${host.username} · ${formatted_time(t[i].created_time)}
                  <br>
                  ${t[i].content}
                  <a href="/tweet/update/${t[i].id}">编辑</a>
                  <a href="/tweet/delete/${t[i].id}">删除</a>
                  <a href="/tweet/${t[i].id}">评论</a>
                  <a href="/tweet/${t[i].id}">转发</a>
                <hr />
                </a>
                `;
                $('#id-div-mytweets').append(template)

            }
        } else {
            for(var i = 0; i < t.length; i++){
                var template = `
                      <a href="/tweet/${t[i].id}" class="list-group-item">
                        ${host.username} · ${formatted_time(t[i].created_time)}
                        <br>
                        ${t[i].content}
                        <a href="/tweet/${t[i].id}">评论</a>
                        <a href="/tweet/${t[i].id}">转发</a>
                      <hr />
                      </a>
                    `;
                $('#id-div-mytweets').append(template)
                }
                }
}


var followee_tweets_template = function(followee_tweets, host, visitor){
    var t = followee_tweets
            for(var i = 0; i < t.length; i++){
                var template = `
                      <a href="/tweet/${t[i].id}" class="list-group-item">
                        ${host.username} · ${formatted_time(t[i].created_time)}
                        <br>
                        ${t[i].content}
                        <a href="/tweet/${t[i].id}">评论</a>
                        <a href="/tweet/${t[i].id}">转发</a>
                      <hr />
                      </a>
                    `;
                $('#id-div-followeetweets').append(template)
                }
              }
