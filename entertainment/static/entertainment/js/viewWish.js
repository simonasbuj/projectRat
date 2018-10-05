//VARIABLES
wishModal = $('#wishInfoModal');

var lastViewedWish = 0;

//FUNCTIONS
function viewWish(){
    selectedWish = $(this).attr('wish_id');

    if(lastViewedWish != selectedWish){
        console.log("API CALL");
        wishModal.find(".modal-body").html("WISH ID: " + selectedWish);

        lastViewedWish = selectedWish;
    }

    wishModal.modal();

}


//EVENT LISTENERS
$(".wish").on("click", viewWish);

/* function openWishInfo(){
    $(".wish").click(function(e) {
        console.log("paspaudei wishh")
        $('#wishInfoModal').modal()
    })
} */