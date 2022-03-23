function link(url) {
    window.location.href = url
}

function find_parent_until(_this, tag) {
    var parent = _this.parentNode;
    while (parent.tagName != tag) {
        parent = parent.parentNode;
    }
    return parent
}

function submit(url, submit_id) {
    var html_obj = $.ajax({url: url, type: "POST", async: false, data: $("#" + submit_id).serialize()});
    console.log(html_obj.responseText)
    return html_obj.responseText
}

function submit_get(url, submit_id) {
    console.log($("#" + submit_id)[0])
    var html_obj = $.ajax({url: url, type: "GET", async: false, data: $("#" + submit_id).serialize()});
    return html_obj.responseText
}

function refresh_submit(url, submit_id) {
    submit(url, submit_id)
    location = location
}

function get(url) {
    htmlobj = $.ajax({url: url, async: false});
    return htmlobj.responseText
}

function get_alert(url) {
    toast(get(url))
}

function get_change_button(url, _this) {
    var js = $.parseJSON(get(url))
    if (js.status) {
        $(_this).text("是")
    } else {
        $(_this).text("否")
    }
}

function get_change(data, in_sel, ele, url) {
    var html = $(get(url));//jquery
    var children = $(html).get(0).children//dom
    toast("已" + data.textContent.trim() + children[0].textContent + "用户")
    var tr = find_parent_until(data, in_sel)
    $(tr).html($(children))
}

function toast(msg, duration) {
    duration = isNaN(duration) ? 1000 : duration;
    var m = document.createElement('div');
    m.innerHTML = msg;
    m.style.cssText = "max-width:60%;min-width: 150px;padding:0 14px;height: 40px;color: rgb(255, 255, 255);line-height: 40px;text-align: center;border-radius: 4px;position: fixed;top: 50%;left: 50%;transform: translate(-50%, -50%);z-index: 999999;background: rgba(0, 0, 0,.7);font-size: 16px;";
    document.body.appendChild(m);
    setTimeout(function () {
        var d = 0.5;
        m.style.webkitTransition = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
        m.style.opacity = '0';
        setTimeout(function () {
            document.body.removeChild(m)
        }, d * 1000);
    }, duration);
}

// function test() {
//     var post_data = []
//     var trs = $("#table").children() //所有t'r
//     for (const tr in trs) {
//         //遍历trs
//         if ($(tr).children()[0]) {//如果这行tr的第一个td 也就是input 是被选中的话
//             //你如果需要数量的话可以继续找数据
//             post_data.append({$(tr).id = $(tr).filter(".shuliang")})//按python的后端接口构造postdata就好了
//
//         }
//     }
//     ajax.post("/xxx", post_data) //post提交
// }