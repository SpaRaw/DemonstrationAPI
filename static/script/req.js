function simPostRequest() {
    const url = 'http://localhost:5000/api/post/'
    prio = document.getElementById("prio").value;
    data = document.getElementById("data").value;
    durations = document.getElementById("duration").value;

    if (prio == '') {
        prio = 10;
    }

    if (data == '') {
        data = 'No Data was sent, this is a standart input'
    }

    if (durations == '') {
        durations = 1000;
    }

    fetch("127.0.0.1:5000/api/post/hallo")
}

function simGetResponse(){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET', 'http://localhost:5000/api/get/', false);

    alert(xmlHttp.responseText);
}