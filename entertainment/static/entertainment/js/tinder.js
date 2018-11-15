//variables
var rldBtn = document.getElementById("rldBtn");
var noBtn = document.getElementById("noBtn");
var yesBtn = document.getElementById("yesBtn");

//functions
function likeBook(){
    data = {bookId: bookId};
    return fetch(likeUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrf,
            "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify(data)
    })
    .then(response => {
            if (response.ok){
                location.reload()
            }else{
                throw new Error("kažaks ne taip");
            }
        }
    );
}

function dislikeBook(){
    data = {bookId: bookId};
    return fetch(dislikeUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrf,
            "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify(data)
    })
    .then(response => {
            if (response.ok){
                location.reload()
            }else{
                throw new Error("kažaks ne taip");
            }
        }
    );
}

//listeners
rldBtn.addEventListener("click", function(){
    location.reload();
});

noBtn.addEventListener("click", dislikeBook);
yesBtn.addEventListener("click", likeBook);
