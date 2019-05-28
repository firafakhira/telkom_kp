var input = document.getElementById("kolomInput");
    input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("cari").click();
    }
});