$(document).ready(function () {
    //CKEDITOR
    CKEDITOR.replace('#blog');
    //GET QUOTES
    getQuotes()
    //REGISTER USER
    $("#registerBtn").click(function (e) {
        e.preventDefault();
        $.ajax({
            data: {
                full_name: $('#fullName').val(),
                email: $('#email').val(),
                password: $('#password').val()
            },
            type: 'POST',
            url: 'users'
        }).done(function (data) {
            alert("Registration completed successfully!")
            $('#fullName').val('')
            $('#email').val(''),
                $('#password').val('')
            location.reload()
        });
    });
    //GET QUOTES
    function getQuotes() {
        $.get("http://quotes.stormconsultancy.co.uk/random.json", function (data) {
            $(".quote").text('"' + data.quote + '"');
            $(".author").text("-" + data.author)
        })
    }

    //SUBMIT BLOG
    $("#submit-blog").click(function (e) {
        e.preventDefault();
        console.log(CKEDITOR.instances['blog'].getData())
        $.ajax({
            data: {
                title: $('#blog-title').val(),
                description: CKEDITOR.instances['blog'].getData(),
                user: $('#user').val()
            },
            type: 'POST',
            url: 'create-blog'
        }).done(function (data) {
            alert("Blog created successfully");
            $('#title').val('')
            $('#blog').val('')
            // getSubCategory()
            location.reload()
        });
    });
    //OPEN COMMENTS 
    $(".comment-btn").click(function (e) {
        e.preventDefault()
        let id = $(this).data("id");
        $("#comment-form" + id).css({ "display": "block" })
    })
    //SUBMIT COMMENT
    $(".submit-comment").click(function (e) {
        e.preventDefault();
        let id = $(this).data("id")
        $.ajax({
            url: 'comments',
            method: 'POST',
            data: {
                description: $("#comment" + id).val().trim(),
                blog: id
            },
            success: function (data) {
                alert("Comment created successfully");
                $("#comment" + id).val('')
                // getSubCategory()
                location.reload()
            }
        })

    })
    //READ COMMENTS
    $(".read-comments-btn").click(function (e) {
        let id = $(this).data("id");
        $("#read-comment" + id).css({ "display": "block" })
    })
    //DELETE COMMENTS
    $(".delete-comment-btn").click(function (e) {
        e.preventDefault();
        if (confirm("Are you sure you want to delete this record")) {
            let id = $(this).data("id")
            $.ajax({
                url: 'delete-comments/' + id,
                method: 'POST',
                data: {},
                success: function (data) {
                    if (data == 'success') {
                        alert("Comment deleted successfully");
                    } else {
                        alert("Record delete failed")
                    }
                    location.reload()
                }
            })
        }
    })
    //DELETE BLOG
    $(".delete-blog-btn").click(function (e) {
        e.preventDefault();
        if (confirm("Are you sure you want to delete this record ?")) {
            let id = $(this).data("id")
            $.ajax({
                url: 'delete-blog/' + id,
                method: 'POST',
                data: {},
                success: function (data) {
                    if (data == 'success') {
                        alert("Comment deleted successfully");
                    } else {
                        alert("Record delete failed")
                    }
                    location.reload()
                }
            })
        }
    })
});