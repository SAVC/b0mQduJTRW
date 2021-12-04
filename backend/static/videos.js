$(document).ready(function () {
    $.get("/videos-head").success(function (result) {
        console.log(result)
        for (const video of JSON.parse(result)) {
            $("#playlist")[0].innerHTML += '<li id="liId' + video['id'] + '">' +
                '<a href="">' + video['id'] + '. ' + video['filename'] + '</a>' +
                '<a href="'+ EDITOR + video['id'] +'"><img src="../static/images/edit.svg" class="download-icon"></a>' +
                '<a href="' + DOWNLOAD_URL + video['id'] + '"><img src="../static/images/download-button.svg" class="download-icon"></a>' +
                '<a href="" onclick="deleteVideo(' + video['id'] + ')"><img src="../static/images/remove.svg" class="download-icon"></a>' +
                '<p><audio controls="" id="audio" type="audio/wav"><source type="audio/wav" src="/audio/' + video['id'] + '"></audio></p>' +
                '</li>'
        }
    });
});

function deleteVideo(id) {
    $.ajax({
        url: VIDEO_URL + id,
        type: 'DELETE',
        success: function (result) {
            console.log("Entity id=" + id + " was deleted")
            $("#liId" + id).remove();
        }
    });
}