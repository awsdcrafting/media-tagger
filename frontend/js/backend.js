var backend;
new QWebChannel(qt.webChannelTransport, function (channel) {
    backend = channel.objects.backend;
});

document.getElementById("header").addEventListener("click", function () {
    backend.foo();
});

document.getElementById("p").addEventListener("click", function () {
    let img = document.createElement("img")
    img.src = "D:\\Projects\\tools\\media-tagger\\images\\Avatar_Dr_Scissi.jpg"
    document.getElementById("cont").appendChild(img)
    backend.foo()
});