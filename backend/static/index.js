const UPLOAD_URL = "http://localhost:5000/upload";
const DOWNLOAD_URL = "http://localhost:5000/download/";
const VIDEO_URL = "http://localhost:5000/video/";
const EDITOR = "http://localhost:5000/editor/";
const TEXT_MAX_LENGTH = 50;

function uploadClick() {
    $('#fileToUpload').click();
    $('input[name=fileToUpload]').change(function (ev) {
        uploadFile();
    });
}

function uploadFile() {
    let myFileInput = document.getElementById("fileToUpload");

    let data = new FormData();
    data.append('file', myFileInput.files[0], myFileInput.files[0].name);
    data.append("aggressive", $("#levels")[0].value);
    data.append("lang", $("#models")[0].value);

    let xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            console.log(this.responseText);
            let responseDto = JSON.parse(this.responseText);
            let text = responseDto.text.length > TEXT_MAX_LENGTH ? responseDto.text.substr(0, TEXT_MAX_LENGTH) + "..." : responseDto.text;
            $("#result").text('Результат: ' + text);
            $("#downloadBtn").removeClass("invisible");
            $("#downloadBtn")[0].href = DOWNLOAD_URL + responseDto.id;
        }
    });

    xhr.open("POST", UPLOAD_URL);

    xhr.send(data);
}

$(document).ready(function () {
    $.get("/models").success(function (response) {
        let html = '';
        for (const modelName of JSON.parse(response)) {
            html += '<option value="' + modelName + '">Модель: ' + modelName + '</option>';
        }
        $("#models").html(html);
    })

    $.get("/aggressive/levels").success(function (response) {
        let html = '';
        for (const level of JSON.parse(response)) {
            html += '<option value="' + level + '">Агрессивность обработки: ' + level + '</option>';
        }
        $("#levels").html(html);
    })
});