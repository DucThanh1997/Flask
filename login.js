$(document).ready(function(){
    $("#login").click(function(){
        var username = $('input[name=username]').val();
        var password = $('input[name=password]').val();

        if(username == ""){
            Swal.fire({
                type: 'error',
                title: 'Lỗi',
                text: 'Tên đăng nhập không được để trống'
            })
            return false;
        }

        if(password == ""){
            Swal.fire({
                type: 'error',
                title: 'Lỗi',
                text: 'Mật khẩu không được để trống'
            })
            return false;
        }

        $.ajax({
            type:"POST",
            url: '/login',
            data: $('#login_form').serialize(),
            beforeSend: function() {
                Swal.fire({
                    title: "Xin chờ...",
                    onBeforeOpen: () => {
                        Swal.showLoading();
                    },
                    allowOutsideClick: false
                });
            },
            complete: function() {
                Swal.close()
            },
            success: function(data){
                console.log(data)
                var result = JSON.parse(JSON.stringify(data));
                if(result.status == 'False'){
                    Swal.fire({
                        type: 'error',
                        title: 'Lỗi',
                        text: result.messages,
                    });
                }
                else{
                    Swal.fire({
                        type: 'success',
                        title: 'Thành công',
                        text: 'Đăng nhập thành công',
                        showConfirmButton: false,
                        // timer: 2000
                    }).then(() =>{
                        location.replace('/')
                    })
                };
             }
        });

    });

});

document.addEventListener('keypress', function (e) {
    var key = e.which || e.keyCode;
    if (key === 13 && !$("body").attr("class").includes("swal")) { // 13 is enter
      $("#login").click();
    }
});



