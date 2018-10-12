//VARIABLES
var wishModal = $('#wishInfoModal');
var rangeValue = $("#rangeValue");
var mySlider = document.getElementById("paymentRange");
var paymentForm = document.getElementById("paymentForm");

var lastViewedWish = 0;
var selectedWishId = 0;

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
            // wishModal.find("#wishcontent").html("WISH ID: " + data.id + "<br>WISH PRICE: " + data.price);



            selectedWishId = data.id
            wishModal.find("#timeLeft").html(data.days_left)
            //SLIDERIS
            var maxAmount = parseFloat(Math.round((data.price - data.donated) * 100) / 100).toFixed(2);
            if (maxAmount < 1){
                mySlider.min = maxAmount;
            }
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




//EVENT LISTENERS
$(".wish").on("click", viewWish);
$("#stripeBtn").on("click", processPayment);

/* function openWishInfo(){
    $(".wish").click(function(e) {
        console.log("paspaudei wishh")
        $('#wishInfoModal').modal()
    })
} */



//STRIPE PAYMENTS
var handler = StripeCheckout.configure({
            key: 'pk_test_YuNvTsnJ7v1s9FCREZfVOeeK',
            image: "/static/img/logo-stripe.png",
            locale: 'auto',
        token: function(token) {
            // You can access the token ID with `token.id`.
            // Get the token ID to your server-side code for use.
            //it can be an ajax call

            //create addition input fields for form
            var tokenInput = document.createElement("input");
            var amountInput = document.createElement("input");
            var wishIdInput = document.createElement("input");
            var emailInput = document.createElement("input");

            //hide input fields
            tokenInput.setAttribute("type", "hidden");
            amountInput.setAttribute("type", "hidden");
            wishIdInput.setAttribute("type", "hidden");
            emailInput.setAttribute("type", "hidden");

            //add value and names to inputs
            tokenInput.setAttribute("value", token.id);
            tokenInput.setAttribute("name", "stripe_token");

            amountInput.setAttribute("value", parseFloat(Math.round(mySlider.value * 100) / 100).toFixed(2));
            amountInput.setAttribute("name", "amount");

            wishIdInput.setAttribute("value", selectedWishId);
            wishIdInput.setAttribute("name", "wish_id");

            emailInput.setAttribute("value", token.email);
            emailInput.setAttribute("name", "email");

            //append to form and submit it
            paymentForm.appendChild(tokenInput);
            paymentForm.appendChild(amountInput);
            paymentForm.appendChild(wishIdInput);
            paymentForm.appendChild(emailInput);

            paymentForm.submit();
        }
        });


function processPayment(){

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

    handler.open({
        name: 'Knygų Žiurkė™',
        description: 'Padovanok Knygą',
        panelLabel: 'PERVESTI',
        amount: mySlider.value * 100,
        currency: "EUR",
        allowRememberMe: false,
    });

}

// Close Checkout on page navigation:
window.addEventListener('popstate', function() {
    handler.close();
});
