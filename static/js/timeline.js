var offset = 20;
var limit = 20;
$(document).ready(function(){
        $('#id-button-loadtweets').on('click', function() {
            var username = this.dataset.name
            console.log('username', username);
            var url = `/tweets/json/${username}?offset=${offset}&limit=${limit}`
            console.log('url', url);
            var request = {
                url: url,
                type: 'get',
                contentType: 'application/json',
                success: success

            }
            $.ajax(request);
        })
});


var success = function(data){
    offset += limit;
    console.log('success', data);
    t = data.tweets;
    user = data.user
    owner = data.owner
    template();
};


var template = function(){
    if (user.id === owner.id) {
        for(var i = 0; i < t.length; i++){
            var template = `
                <p>
                    ${t[i].content} --${t[i].created_time}
                    <br>
                    <a href="/tweet/update/${t.id}">编辑</a>
                    <a href="/tweet/delete/${t.id}">删除</a>
                    <a href="/tweets/${t[i].id}">评论</a>
                    <a href="/tweets/${t[i].id}">转发</a>
                </p>
                `;
                $('#id-div-tweets').append(template)

            }
        } else {
            for(var i = 0; i < t.length; i++){
                var template = `
                    <p>
                        ${t[i].content} --${t[i].created_time}
                        <br>
                        <a href="/tweets/${t[i].id}">评论</a>
                        <a href="/tweets/${t[i].id}">转发</a>
                    </p>
                    `;
                $('#id-div-tweets').append(template)
                }
                }
}