$( document ).ready(function() {
    $('[data-toggle="popover"]').popover(); 
    bookmark()
    addComment()
    reply()

    function reply(){
        $(".fa-reply").click(function(e) {
            //get parent div
            let parentComment = $(this).closest(".comment-box")

            changeReplyText(parentComment)
            $('[data-toggle="popover"]').popover(); 
            //move to reply area and focus it boiiiii
            $('html, body').animate({
                scrollTop: $("#reply").offset().top - 200
            }, 1000);            
            $("#newcomment_text").focus();

            $("#dontreply").click(function(e) {
                console.log("bandysim pasalinti reply")
                $(this).closest("div").fadeOut(300, function() { $(this).closest("div").remove(); });
                $('.popover').popover('hide');
                //$(this).closest("div").remove()
                changeIsReply(0)
            });                

        });
    }

    function changeReplyText(parentComment){
        //get coment author
        let author = parentComment.find(".comment-name")
        author = author.text()
        console.log(author)

        //get comment id
        let id = parentComment.attr("comId")
        console.log(id)
        changeIsReply(id)

        //get comment text
        let comment = parentComment.find(".comment-content")
        comment = comment.text().trim()
        console.log(comment)

        let replyText = $("#newcomment")
        replyText.find("div#replyingTo").remove()
        replyText.prepend("<div id='replyingTo'><button id='dontreply' type='button' class='close' aria-label='Close' data-toggle='popover' data-trigger='hover' data-content='Atšaukti' data-placement='top'><span aria-hidden='true'>&times;</span></button><h5>Atsakai į " + author + " komentarą:</h5><p>" + comment + "</p></div>")
    }

    function changeIsReply(id){
        let isReply = $("input[name='isReply']")
        isReply.val(id)
    }

    function bookmark(){
        $("#bookmark").click(function(e) {
            console.log("bandysim bookmarkint")
            let btn = $(this)
            $.ajax({
                url: "{% url 'library:bookmark' book.slug %}",
                /*
                data: {
                    text: $("textarea[name=Status]").val(),
                    Status: 'test'
                },
                dataType : 'json',*/
                success: function(data){
                    console.log(data)
                    console.log(btn.attr('class'))
                    btn.toggleClass('bookmark')
                    btn.toggleClass('bookmarked')
                    if(btn.attr('data-content') == 'Prisiminti'){
                        btn.attr('data-content', 'Pamiršti')
                    } else {
                        btn.attr('data-content', 'Prisiminti')
                    }          
                },
                error: function(data){
                    console.log('nepaejo')
                }
            });
        });
    }

    function addComment(){
        let form = $("#newCommentForm")

        form.submit(function(e){
            e.preventDefault()
            let csrf_token = form.find("[name='csrfmiddlewaretoken']").val()
            let text = form.find("textarea").val().trim()              
            let parentId = form.find("[name='isReply']").val()
            console.log("CSRF: " + csrf_token + "\nTEXT: " + text + "\nPARENDID: " + parentId)
            $.ajax({
                type: 'POST',
                url: form.attr("action"),
                data:{
                    'csrfmiddlewaretoken': csrf_token,
                    'text': text,
                    'parentId': parentId,
                },
                success: function(data){
                    let textarea = form.find("textarea")
                    if(data.error){
                        console.log(data.error)
                        form.find("textarea").addClass("is-invalid")
                    } else if(parentId == 0){                            
                        textarea.removeClass("is-invalid")
                        textarea.val('')
                        let commentDiv = $("#comments-list:first")
                        text = text.replace(/(?:\r\n|\r|\n)/g, '<br>');
                        commentDiv.append("<li><div class='comment-main-level'><div class='comment-avatar'><img src='{{ user.info.avatar.url }}' alt=''></div><div class='comment-box' comId='4'><div class='comment-head'><h6 class='comment-name'><a href='#'>{{ user.username }}</a></h6><span>dabar</span><i class='fa fa-reply' data-toggle='popover' data-trigger='hover' data-content='Atsakyti' data-placement='top'></i></div><div class='comment-content'>" + text + "</div></div></div></li>")
                        $('html, body').animate({
                            scrollTop: commentDiv.find("li").last().offset().top - 800
                        }, 1000);                                                     
                    } else {
                        textarea.removeClass("is-invalid")
                        textarea.val('')
                        let parentCom = $("[comId='"+ parentId +"'")
                        parentCom = parentCom.closest(".reply-list")
                        parentCom.append("<li><div class='comment-main-level'><div class='comment-avatar'><img src='{{ user.info.avatar.url }}' alt=''></div><div class='comment-box' comId='4'><div class='comment-head'><h6 class='comment-name'><a href='#'>{{ user.username }}</a></h6><span>dabar</span><i class='fa fa-reply' data-toggle='popover' data-trigger='hover' data-content='Atsakyti' data-placement='top'></i></div><div class='comment-content'>" + text + "</div></div></div></li>")
                        $('html, body').animate({
                            scrollTop: parentCom.find("li").last().offset().top - 500
                        }, 1000);
                        let replyText = $("#newcomment")
                        replyText.find("div#replyingTo").remove()

                    }
                    reply()
                }                    
            })


        })
    }

});