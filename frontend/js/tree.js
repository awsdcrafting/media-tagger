document.addEventListener('click', function (e) {
    e = e || window.event;
    let target = e.target || e.srcElement
    console.log(target)
    if (!target || !target.classList) {
        return
    }
    if (target.tagName == "ICON") {
        target = target.parentNode
    }
    if (target.tagName == "FOLDER") {
        target.classList.toggle("open")
        console.log(target)
        console.log(target.parentNode)
        target.parentNode.querySelector("ul").classList.toggle("visible")
    }

});