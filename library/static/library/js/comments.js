function spawnCommentBox(id, text, created_by, avatar){
    $("#no_comments").remove()
    let commentsTab = $("#pills-comments")
    html = "\
    <div class='comments-container'>\
        <ul id='comments-list' class='comments-list'>\
            <li>\
            <div class='comment-main-level'>\
                <div class='comment-avatar'><img src='" + avatar + "' alt=''></div>\
                <div class='comment-box' comId='" + id + "'>\
                    <div class='comment-head'>\
                        <h6 class='comment-name by-you'>\
                            <a href='#'>" + created_by + "</a>\
                        </h6>\
                        <span>dabar</span>\
                        <i class='fa fa-reply' data-toggle='popover' data-trigger='hover' data-content='Atsakyti' data-placement='top'></i>\
                    </div>\
                    <div class='comment-content'>\
                        "+ text +"\
                    </div>\
                </div>\
            </div>\
            </li>\
        </ul>\
    </div>\
    ";
    $(html).hide().prependTo(commentsTab).fadeIn(1000)

}

function spawnParentComment(id, text, created_by, avatar){
    let commentsList = $("#comments-list")
    html = "\
    <li>\
        <div class='comment-main-level'>\
            <div class='comment-avatar'><img src='" + avatar + "' alt=''></div>\
            <div class='comment-box' comId='" + id + "'>\
                <div class='comment-head'>\
                    <h6 class='comment-name by-you'><a href='#'>" + created_by  + "</a></h6>\
                    <span>dabar</span>\
                    <i class='fa fa-reply' data-toggle='popover' data-trigger='hover' data-content='Atsakyti' data-placement='top'></i>\
                </div>\
                <div class='comment-content'>\
                    " + text + "\
                </div>\
            </div>\
        </div>\
    </li>\
    ";
    $(html).hide().appendTo(commentsList).fadeIn(1000)
}

function spawnNewChild(id, text, created_by, avatar, parent_id){
    let parentComment = $(".comment-box[comId='" + parent_id + "']")
    parentComment = parentComment.closest("li")

    html = "\
    <ul class='comments-list reply-list'>\
        <li>\
            <div class='comment-avatar'><img src='" + avatar + "' alt=''></div>\
            <div class='comment-box' comId='" + id +"'>\
                <div class='comment-head'>\
                    <h6 class='comment-name by-you'><a href='#'>" + created_by + "</a></h6>\
                    <span>dabar</span>\
                    <i class='fa fa-reply' data-toggle='popover' data-trigger='hover' data-content='Atsakyti' data-placement='top'></i>\
                </div>\
                <div class='comment-content'>\
                    " + text + "\
                </div>\
            </div>\
        </li>\
    </ul>\
    ";
    $(html).appendTo(parentComment)
    $('html, body').animate({
        scrollTop: parentComment.find(".reply-list li:last-child").last().offset().top - 500
    }, 1000);

}

function spawnAnotherChild(id, text, created_by, avatar, parent_id){

    let parentComment = $(".comment-box[comId='" + parent_id + "']")
    parentComment = parentComment.closest("li").find(".reply-list")
    parentComment.show(0)
    parentComment.siblings('.showReplies').remove()
    

    html = "\
    <li>\
        <div class='comment-avatar'><img src='" + avatar + "' alt=''></div>\
        <div class='comment-box' comId='" + id +"'>\
            <div class='comment-head'>\
                <h6 class='comment-name by-you'><a href='#'>" + created_by + "</a></h6>\
                <span>dabar</span>\
                <i class='fa fa-reply' data-toggle='popover' data-trigger='hover' data-content='Atsakyti' data-placement='top'></i>\
            </div>\
            <div class='comment-content'>\
                " + text + "\
            </div>\
        </div>\
    </li>\
    ";
    $(html).appendTo(parentComment)

    $('html, body').animate({
        scrollTop: parentComment.find("li:last-child").last().offset().top - 500
    }, 1000);
}

function showHiddenReplies(){
    $('.showReplies').click(function(e) {
        $(this).siblings(".reply-list").slideDown("slow")
        $(".reply-list", this).slideDown("slow")
        $(this).remove()
    });                

}