// DAFTAR AKUN
$(document).ready(function () {
    $('#registerForm').submit(function (event) {
        event.preventDefault(); // Menghentikan pengiriman form default

        var username = $('#username').val();
        var password = $('#password').val();

        $.ajax({
            type: 'POST',
            url: '/register',
            contentType: 'application/json',
            data: JSON.stringify({ username: username, password: password }),
            success: function (response) {
                alert(response.message); // Tampilkan pesan sukses dari server
                // Redirect atau tindakan lainnya setelah pendaftaran berhasil
            },
            error: function (xhr, status, error) {
                alert(xhr.responseJSON.message); // Tampilkan pesan error dari server
            }
        });
    });
});

// FUNCTION LOGIN
function sign_in() {
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            username: username,
            password: password,
        },
        success: function (response) {
            if (response["result"] === "success") {
                $.cookie("mytoken", response["token"], { path: "/" });
                window.location.replace("/");
            } else {
                alert(response["msg"]);
            }
        },
    });
}