const children = document.getElementsByClassName("toggle-child-button");

[].forEach.call(children, c => {
    c.addEventListener("click", () => {
        childContainer = c.parentElement.nextElementSibling;

        if (childContainer.style.display != "none") {
            childContainer.style.display = "none";
        } else {
            childContainer.style.display = "block";
        }
    }, false);
});