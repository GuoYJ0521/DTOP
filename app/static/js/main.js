// move to the specific position
function toPosition(data) {
    let toPosition = data.getBoundingClientRect().top + scrollY;
    console.log("move to " + toPosition)
    window.scrollTo({
        top: toPosition - 80,
        behavior: 'smooth'
    });
}

document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("#collapse-left").addEventListener("click", function() {
        let containerLeft = document.querySelector("#container-left");
        containerLeft.classList.toggle("active");
        
        let arrowLeft = containerLeft.querySelector("i");
        arrowLeft.classList.toggle("bi-arrow-bar-right");
    });

    document.getElementById("collapse-right").addEventListener("click", function() {
        let containerRight = document.getElementById("container-right");
        containerRight.classList.toggle("active");
        
        let arrowRight = containerRight.querySelector("i");
        if (arrowRight.classList.contains("bi-arrow-bar-right")) {
            arrowRight.classList.remove("bi-arrow-bar-right");
            arrowRight.classList.toggle("bi-arrow-bar-left");
        }
        else {
            arrowRight.classList.remove("bi-arrow-bar-left");
            arrowRight.classList.toggle("bi-arrow-bar-right");
        }
    });
});
