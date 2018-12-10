
var takeDate = document.getElementById("take_date");
var returnDate = document.getElementById("return_date");
var reserveBtn = document.getElementById("reserveBtn");


function makeReservation(e){
    var dstart = new Date(takeDate.value);
    var dend = new Date(returnDate.value);
    if (dstart > dend){
        takeDate.classList.add("is-invalid");
        returnDate.classList.add("is-invalid");
        e.preventDefault();
    }

}


reserveBtn.addEventListener("click", makeReservation);
