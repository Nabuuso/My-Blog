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
            $(".quote").text('"'+data.quote+'"');
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
                description:CKEDITOR.instances['blog'].getData(),
                user:$('#user').val()
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
});