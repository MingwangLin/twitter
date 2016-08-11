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
            console.log('上传成功', file.name);
        },
        error: function() {
            console.log('上传失败', file.name);
        }
    });
};
