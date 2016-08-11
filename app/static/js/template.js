var tweet_template = `
                      <button class="btn btn-default btn-xs pull-right button-comments">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                        </span>
                        评论
                        </button>
                        <button class="btn btn-default btn-xs pull-right id-button-retweets">
                        <span class="glyphicon glyphicon-share" aria-hidden="true">
                        </span>
                        转发
                      </button>
                      <div class="clearfix div-commentarea">
                      </div>
                      `

var none_template = `<p class="none text-center">
                      <span class="glyphicon glyphicon-info-sign">
                      </span>
                      空空如也，说点什么吧。
                    </p>
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
                      <input class="form-control" name="content" id="id-text-addcomment" placeholder="评论点什么">
                      <span class="input-group-btn">
                      <button class="btn btn-default pull-right button-addcomment" type="button">
                      <span class="glyphicon glyphicon-send" aria-hidden="true">
                      </span>
                      发表评论
                      </button>
                      </span>
                      </div>
                      `
