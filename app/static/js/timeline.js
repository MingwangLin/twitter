var mytweets_offset = 0;
var mytweets_limit = 20;
var followeetweets_offset = 0;
var followeetweets_limit = 20;
// @通知偏移量
var ats_offset = 0;
var ats_limit = 20;

$(document).ready(function(){
        username = $('#id-button-load-mytweets').attr('data-name');
        log('username', username)
        var mytweets_url = '/tweets/' + username + '?offset=' + mytweets_offset + '&limit=' + mytweets_limit
        var followeetweets_url = '/followee_tweets/' + username + '?offset=' + followeetweets_offset + '&limit=' + followeetweets_limit
        var ats_url = '/ats/' + username + '?offset=' + ats_offset + '&limit=' + ats_limit
        show_tweets(mytweets_url, mytweets_response);
        show_tweets(followeetweets_url, followeetweets_response)
        show_notification(ats_url, notification_response)
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
    var tabAction = function (show_mytweets, show_followeetweets, show_ats) {
        $('#id-div-mypage').toggle(show_mytweets);
        $('#id-div-followeepage').toggle(show_followeetweets);
        $('#id-div-notificationpage').toggle(show_ats);
    };

    $('#id-a-mytweets').on('click', function() {
        var show_ats = false;
        var show_followeetweets = false;
        var show_mytweets = true;
        tabAction(show_mytweets, show_followeetweets, show_ats);
    });
    $('#id-a-followeetweets').on('click', function() {
        var show_ats = false;
        var show_followeetweets = true;
        var show_mytweets= false;
        tabAction(show_mytweets, show_followeetweets, show_ats);

    });
    $('#id-a-notification').on('click', function() {
        var show_ats = true;
        var show_followeetweets = false;
        var show_mytweets= false;
        tabAction(show_mytweets, show_followeetweets, show_ats);
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
    $('#id-button-load-notifications').on('click', function(){
        var ats_url = '/ats/' + username + '?offset=' + ats_offset + '&limit=' + ats_limit
        show_tweets(ats_url, ats_response);
    });

    $('#id-button-addtweet').on('click', add_newtweet);

};

var show_tweets = function(url,response){
  get(url, response);
}

var show_notification = function(url,response){
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

var notification_response = function(data){
  if(data.success) {
    ats_offset += mytweets_limit;
    log('success', data);
    var ats = data.ats;
    var host = data.host
    var visitor = data.visitor
    ats_template(ats, host, visitor);
}else {
  log('请求失败');
}
};

var my_tweets_template = function(tweets, host, visitor){
    var t = tweets
    if (visitor.id === host.id) {
        for(var i = 0; i < t.length; i++){
            var template = `
                  <div class="well">
                  ${host.username} · ${formatted_time(t[i].created_time)}
                  <br>
                  ${t[i].content}
                  ${basic_template}
                </div>
                <hr />

                `;
                $('#id-div-mytweets').append(template)

            }
        } else {
            for(var i = 0; i < t.length; i++){
                var template = `
                      <div class="well">
                        ${host.username} · ${formatted_time(t[i].created_time)}
                        <br>
                        ${t[i].content}
                        ${basic_template}
                      </div>
                      <hr />
                    `;
                $('#id-div-mytweets').append(template)
                }
                }
}


var followee_tweets_template = function(followee_tweets, host, visitor){
    var t = followee_tweets
            for(var i = 0; i < t.length; i++){
                var template = `
                      <div class="well">
                        ${t[i].user_name} · ${formatted_time(t[i].created_time)}
                        <br>
                        ${t[i].content}
                        ${basic_template}
                      </div>
                      <hr/>
                    `;
                $('#id-div-followeetweets').append(template)
                }
              }

var ats_template = function(ats, host, visitor){
  var t = ats
  var words = '在微博@了你'
    for(var i = 0; i < t.length; i++){
        var template = `
            <div class="well">
              ${t[i].sender_name} ${words}
              <a href="#" class="list-group-item">
                ${t[i].sender_name} · ${formatted_time(t[i].created_time)}
                <br>
                ${t[i].tweet_content}
                ${basic_template}
    </a>
              </div>
            `;
        $('#id-div-notification').append(template)
        }
      }

var basic_template = `<button class="btn btn-default pull-right" id="id-button-addtweet">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                        </span>
                        评论
                        </button>
                        <button class="btn btn-default pull-right" id="id-button-addtweet">
                        <span class="glyphicon glyphicon-share" aria-hidden="true">
                        </span>
                        转发
                      </button>`
