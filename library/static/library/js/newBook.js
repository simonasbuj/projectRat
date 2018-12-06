var newWishBtn = document.getElementById("newWishBtn");
var newWriterBtn = document.getElementById("newWriterBtn");


//functions
function addNewWriter(){
        //console.log( $("input[name=writers]") )
        var writerInputs = $("input[name=writers]");
        var isValid = true;
        writerInputs.each(function( index ) {
            if(!$(this).val() || $(this).val().length < 6){
                $(this).addClass("is-invalid");
                isValid = false;
            }
        });

        if(isValid){
            var htmls = "";
            htmls += `
            <div class="inputWrapper">
                <div class='form-group mb-1'>
                    <input type='text' class='form-control'  name='writers' placeholder='Autoriaus vardas ir pavardė' onchange='removeInvalid(this)'>
                    <i class="fas fa-times xbtn"></i>
                </div>
            </div>
            `;
            $(htmls).hide().appendTo(writersDiv).fadeIn(1000);

        }
}

function addNewWish(e){

    var isValid = true;
    var writerInputs = $("input[name=writers]");
    var bookName = $("input[name=bookName]");
    var cat = $("select[name=newBookCategory]");

    if(!bookName.val()){
        bookName.addClass("is-invalid");
        isValid = false;
    }

    writerInputs.each(function( index ) {
        if(!$(this).val() || $(this).val().length < 6){
            $(this).addClass("is-invalid");
            isValid = false;
        }
    });

    if(!cat.val() || cat.val() == 0){
        console.log("OKK");
        cat.addClass("is-invalid");
        isValid = false;
    }

    if(!isValid) e.preventDefault();   

}

function removeInvalid(){
    $(arguments[0]).removeClass("is-invalid");
}

function removeWriter(){
    $(this).closest(".inputWrapper").remove();
}

//EVENT LISTENERS
newWishBtn.addEventListener("click", function(){
    $('#newBookModal').modal();
});

newWriterBtn.addEventListener("click", addNewWriter);
$("#writersDiv").on("click", ".xbtn", removeWriter);

$("#newWishFormBtn").on("click", addNewWish);
