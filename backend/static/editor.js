$(document).ready(function () {
    console.log(id);
    $("#audio")[0].innerHTML = '<p><audio controls="" id="audio" type="audio/wav"><source type="audio/wav" src="/audio/' + id + '"></audio></p>'
    $.get("/videos/" + id).success(function (response) {
        $("#editor")[0].innerHTML = JSON.parse(response).content;
        ClassicEditor
            .create(document.querySelector('#editor'))
            .catch(error => {
                console.error(error);
            });
    });
});

function update() {
    let data = {"text": $(".ck-content").text()}

    $.ajax({
        type: 'PUT',
        url: '/video/' + id,
        contentType: 'application/json',
        data: JSON.stringify(data), // access in body
    }).done(function () {
        console.log('SUCCESS');
    }).fail(function (msg) {
        console.log('FAIL');
    }).always(function (msg) {
        console.log('ALWAYS');
    });
}