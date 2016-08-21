var tweet_template = function(avatar_path, tweet, comments_length){
  log('4', tweet)
  return template =
                `
                  <div class="media list-group-item tweetbox">
                  <div class="media-left">
                    <a href="#">
                      <img class="media-object img-circle" src="${avatar_path}" alt="32x32" style="width: 32px; height: 32px;">
                    </a>
                  </div>
                  <div class="media-body clearfix singletweet" data-id="${tweet.id}">
                    ${href_for_personalpage(tweet.user_name)} · ${formatted_time(tweet.created_time)}
                    <br>
                    ${tweet.content}
                    ${reposted_tweet_template(tweet.original_tweet)}
                  <div class="btn-group bottom-right " role="group" aria-label="...">
                  <button type="button" class="btn btn-default btn-xs button-comments">
                    <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                    </span>
                    <span class="comments-toggle">评论${comments_length}</span>
                    <span class="comments-toggle" style="display: none">收起</span>
                  </button>
                  <button type="button" class="btn btn-default btn-xs button-reposts">
                    <span class="glyphicon glyphicon-share" aria-hidden="true">
                    </span>
                    <span class="reposts-toggle">转发</span>
                    <span class="reposts-toggle" style="display: none">收起</span>
                  </button>
                  </div>
                  <div class="clearfix div-repostarea" style="display: none">
                  ${addrepost_textarea_template}
                  </div>
                  <div class="clearfix div-commentarea">
                  </div>
                  <hr />
                  </div>
                  </div>
                `
              };

var reposted_tweet_template = function(tweet){
  log('tweet3', tweet[0])
  if (tweet.length != 0) {
    return template =
                `
                  <div class="media list-group-item well reposted_tweet clearfix">
                    <div class="media-left">
                    <a href="#">
                      <img class="media-object img-circle" src="${tweet[0].avatar}" alt="32x32" style="width: 32px; height: 32px;">
                    </a>
                  </div>
                  <div class="media-body clearfix singletweet" data-id="${tweet[0].id}">
                    ${href_for_personalpage(tweet[0].user_name)} · ${formatted_time(tweet[0].created_time)}
                    <br>
                    <p class="font-small">
                    ${tweet[0].content}
                    </p>
                  <div class="btn-group bottom-right" role="group" aria-label="...">
                  <button type="button" class="btn btn-default btn-xs button-comments">
                    <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                    </span>
                    <span class="comments-toggle">评论</span>
                    <span class="comments-toggle" style="display: none">收起</span>
                  </button>
                  <button type="button" class="btn btn-default btn-xs button-reposts">
                    <span class="glyphicon glyphicon-share" aria-hidden="true">
                    </span>
                    <span class="reposts-toggle">转发</span>
                    <span class="reposts-toggle" style="display: none">收起</span>
                  </button>
                  </div>
                  <div class="clearfix div-repostarea" style="display: none">
                  ${addrepost_textarea_template}
                  </div>
                  <div class="clearfix div-commentarea">
                  </div>
                  <hr />
                  </div>
                  </div>
                `
              }else {
                return template = ``
              }

              };

var none_template = `<div class="none transbox">
                      <p class="text-center ">
                        你还未发表任何微博
                      </p>
                    </div>
                    `

var nomore_template = `<p class="nomore text-center">
                    <span class="glyphicon glyphicon-info-sign">
                    </span>
                    没有更多了
                    </p>
                    `
var addcomment_textarea_template = `
                      <hr />
                      <div class="input-group">
                      <input class="form-control text-addcomment" name="content" placeholder="评论点什么">
                      <span class="input-group-btn">
                      <button class="btn btn-default pull-right button-addcomment" type="button">
                      <span class="glyphicon glyphicon-send" aria-hidden="true">
                      </span>
                      发表评论
                      </button>
                      </span>
                      </div>
                      `
var addrepost_textarea_template = `
                      <hr />
                      <div class="input-group">
                      <input class="form-control text-addrepost" name="content" placeholder="说点什么">
                      <span class="input-group-btn">
                      <button class="btn btn-default pull-right button-addrepost" type="button">
                      <span class="glyphicon glyphicon-share" aria-hidden="true">
                      </span>
                      转发
                      </button>
                      </span>
                      </div>
                      `
