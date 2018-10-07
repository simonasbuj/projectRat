//VARIABLES
var wishModal = $('#wishInfoModal');
var rangeValue = $("#rangeValue");
var mySlider = document.getElementById("paymentRange");
var paymentForm = document.getElementById("paymentForm");

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
            /* wishModal.find(".modal-body").find(".row").html("WISH ID: " + data.id + "<br>WISH PRICE: " + data.price); */
            wishModal.find("#wishcontent").html("WISH ID: " + data.id + "<br>WISH PRICE: " + data.price);


            //SLIDERIS
            var maxAmount = parseFloat(Math.round((data.price - data.donated) * 100) / 100).toFixed(2);
            console.log("MAX AMOUNT: " + maxAmount);
            mySlider.max = maxAmount;
            mySlider.value = maxAmount;
            rangeValue.html(maxAmount);            

            //select comments tab to be active and show modal
            $('#pills-comments-tab').tab('show');
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

//this function shows amount on range change
function showAmount(value){
    rangeValue.html(parseFloat(Math.round(value * 100) / 100).toFixed(2));
}

function processPayment(){
    console.log("STRIPE FOR: " + mySlider.value * 100);
    nameField = paymentForm.elements["payerFirstName"];
    lastnameField = paymentForm.elements["payerLastName"];
    if(nameField){
        var isValid = true;
        if(nameField.value == null || nameField.value == ""){
            nameField.classList.add("is-invalid");
            isValid = false;
        }
        if(lastnameField.value == null || lastnameField.value == ""){
            lastnameField.classList.add("is-invalid");
            isValid = false;
        }
        if(!isValid) return;
    }
    
    console.log("PAYMENT RPOCESSING");
    
}


//EVENT LISTENERS
$(".wish").on("click", viewWish);
$("#stripeBtn").on("click", processPayment);

/* function openWishInfo(){
    $(".wish").click(function(e) {
        console.log("paspaudei wishh")
        $('#wishInfoModal').modal()
    })
} */