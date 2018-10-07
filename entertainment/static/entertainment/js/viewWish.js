//VARIABLES
wishModal = $('#wishInfoModal');

var lastViewedWish = 0;

//FUNCTIONS
function viewWish(){
    selectedWish = $(this).attr('wish_id');

    if(lastViewedWish != selectedWish){
        console.log("API CALL");

        fetch(selectedWish)
        .then((resp) => {
            if(resp.ok){
                return resp.json()
            } else {
                throw new Error("API call returned with and error");
            }
        })
        .then((data) => {
            console.log(data);
            wishModal.find(".modal-body").html("WISH ID: " + data.id + "<br>WISH PRICE: " + data.price);
            wishModal.modal();
        })
        .catch(function(error){
            console.log(error);  
/*             document.body.innerHTML += `
                <div class="alert alert-danger alert-dismissible fade show" id="myAlert" role="alert">
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="alert-heading">KLAIDA!</h4>
                    <p>Žiurkė sugraužė laidus! Bandykite perkrauti puslapį.</p>
                </div>
            `;    */ 
        });

        lastViewedWish = selectedWish;
    }else{
        wishModal.modal();
    }

    

}


//EVENT LISTENERS
$(".wish").on("click", viewWish);

/* function openWishInfo(){
    $(".wish").click(function(e) {
        console.log("paspaudei wishh")
        $('#wishInfoModal').modal()
    })
} */