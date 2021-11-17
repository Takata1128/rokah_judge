$(function () {
    // button
    var btn_clone = $('#btn-clone');  // 追加ボタン
    var btn_remove = $('#btn-remove');  // 削除ボタン
    // clone
    btn_clone.click(function () {
        var last_id = $('.testcase_index').last();
        last_id
            .clone()  // クローン
            .val('')  // valueもクローンされるので削除する
            .insertAfter(last_id);
        var last_input = $('.testcase_input').last();  // 最後尾にあるinput
        last_input
            .clone()  // クローン
            .val('')  // valueもクローンされるので削除する
            .insertAfter(last_input);
        var last_output = $('.testcase_output').last();  // 最後尾にあるinput
        last_output
            .clone()  // クローン
            .val('')  // valueもクローンされるので削除する
            .insertAfter(last_output);
        var last_is_sample = $('.is_sample').last();
        last_is_sample
            .clone()
            .insertAfter(last_is_sample);

        if ($('.testcase_input').length >= 2) {
            $(btn_remove).show();  // inputが2つ以上あるときに削除ボタンを表示
        }
    });
    // remove
    btn_remove.click(function () {
        $('.testcase_index').last().remove();
        $('.testcase_input').last().remove();
        $('.testcase_output').last().remove();
        $('.is_sample').last().remove();
        if ($('.testcase_input').length < 2) {
            btn_remove.hide();  // inputが2つ未満のときに削除ボタンを非表示
        }
    });

    // validationチェック
    (function () {
        window.addEventListener('load', function () {
            var forms = document.getElementsByClassName('add-problem');
            var validation = Array.prototype.filter.call(forms, function (form) {
                form.addEventListener('submit', function (event) {
                    if (form.checkValidity() === false) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }, false);
            });
        }, false);
    })();
});