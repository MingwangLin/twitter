var upload = function(file) {
    var fd = new FormData();
    fd.append('uploaded', file);
    $.ajax({
        url: '/upload/avatars',
        method: 'post',
        contentType: false,
        processData: false,
        data: fd,
        success: function(r) {
          if (r.success) {
            var url = r.data;
            window.location.href = url;
          } else {
            log('服务器提了一个问题');
          }
        },
        error: function() {
            console.log('上传失败', file.name);
        }
    });
};
