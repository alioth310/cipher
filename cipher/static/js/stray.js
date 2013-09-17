$(document).ready(function() {
    $('a[name=user-del-btn]').click(function(event) {
        var r = confirm("删除用户?");
        var id = this.id.replace(/del-/, '');
        if (r == true) {
            jQuery.ajax({
                url: '/admin/user/delete',
                type: 'POST',
                data: {
                    id: id,
                    _xsrf: getCookie('_xsrf')
                },
                dataType: 'text',
                success: function(data, status, xhr) {
                    if (data == '0') {
                        alert("删除成功");
                        var line = $('#user-' + id);
                        line.fadeOut(300, function() {
                            line.remove();
                        });
                    } else if (data == '2') {
                        alert("不能删除管理员用户");
                    } else {
                        alert("删除失败");
                    }
                }
            });
        }
    });

});

function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}
