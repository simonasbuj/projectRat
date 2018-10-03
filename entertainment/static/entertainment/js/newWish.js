//variables
var newWishBtn = document.getElementById("newWishBtn");
var newWriterBtn = document.getElementById("newWriterBtn");
var writersDiv = document.getElementById("writersDiv");
var booktitleinput = document.getElementsByName("bookName")[0];

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

function removeInvalid(){
    $(arguments[0]).removeClass("is-invalid");
}

function removeWriter(){
    $(this).closest(".inputWrapper").remove();
}

function getBooks(){
    //console.log(this.value);
    bookSuggestions = $("#bookSuggestions");
    bookSuggestions.html("");
    if(this.value){

        var api_url = '/api/books/search/' + this.value;
        fetch(api_url)
        .then((res) => res.json())
        .then((data) => {
            let output = '';
            data.forEach(function(book){
                output += `
                    <div class="col-3 mb-2 pl-0">
                        <a href="${book.url}">
                            <img class="w-100 book" src="${book.cover_url}" data-toggle='popover' data-trigger='hover' data-content='${book.title}' data-placement='top'>
                        </a>
                    </div>
                `;
            });            
            $(output).hide().appendTo(bookSuggestions).fadeIn(1000);
            $('[data-toggle="popover"]').popover();
            //document.getElementById("bookSuggestions").innerHTML = output;
        });

    } //endif
}

function addNewWish(e){
    
    var isValid = true;
    var writerInputs = $("input[name=writers]");
    var bookName = $("input[name=bookName]");
    var comment = $("textarea[name=newWishComment]");

    if(!bookName.val()){
        bookName.addClass("is-invalid");
        isValid = false;
    }

    if(!comment.val() || comment.val().length < 10 ){
        comment.addClass("is-invalid");
        isValid = false;
    }

    writerInputs.each(function( index ) {
        if(!$(this).val() || $(this).val().length < 6){
            $(this).addClass("is-invalid");
            isValid = false;
        }
    });

    if(!isValid) e.preventDefault();

}

//EVENT LISTENERS
newWishBtn.addEventListener("click", function(){
    $('#newWishModal').modal()
});

newWriterBtn.addEventListener("click", addNewWriter);

//writersDiv.addEventListener("click", removeWriter);
$("#writersDiv").on("click", ".xbtn", removeWriter);

booktitleinput.addEventListener("change", getBooks);

$("#newWishFormBtn").on("click", addNewWish);
