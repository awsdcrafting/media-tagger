const left_resizer = document.querySelector("#left-resizer")
const left_sidebar = document.querySelector("#folder-tree-container")
const right_resizer = document.querySelector("#right-resizer");
const right_sidebar = document.querySelector("#action-container");

left_sidebar.style.flexBasis = '20vw';
right_sidebar.style.flexBasis = '20vw';

left_resizer.addEventListener("mousedown", (event) => {
    document.addEventListener("mousemove", left_resize, false);
    document.addEventListener("mouseup", () => {
        document.removeEventListener("mousemove", left_resize, false);
    }, false);
});

right_resizer.addEventListener("mousedown", (event) => {
    document.addEventListener("mousemove", right_resize, false);
    document.addEventListener("mouseup", () => {
        document.removeEventListener("mousemove", right_resize, false);
    }, false);
});

function left_resize(e) {
    const size = `${e.x}px`;
    left_sidebar.style.flexBasis = size;
}

function right_resize(e) {
    const size = `calc(100vw - ${e.x}px)`;
    right_sidebar.style.flexBasis = size;
}


