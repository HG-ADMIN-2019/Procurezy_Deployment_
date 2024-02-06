    nav_bar_shop()
    
    // 
    $('#change_password').click(function() {
        $('#password_change_form').trigger('reset')
        $('#success_message').hide()
        $('#error_message').hide()
        $('#id_old_password').addClass('form-control')
        $('#id_new_password1').addClass('form-control')
        $('#id_new_password2').addClass('form-control')
        $('#change_password_pop_up').modal('show')
    })


    // password change form 
    $('#password_change_form').submit(function (e) {
        e.preventDefault();
        old_password = $('#id_old_password').val()
        new_password1 = $('#id_new_password1').val()
        new_password2 = $('#id_new_password2').val()
        if (new_password1 != new_password2) {
            $('#error_message').html('Passwords do not match')
            $('#success_message').hide()
            $('#error_message').show()
            return
        }
        $('#change_password_pop_up').modal('hide')
        $.ajax({
            type: 'POST',
            url: change_password_url,
            data: {
                old_password: old_password,
                new_password1: new_password1,
                new_password2: new_password2,
            },
            success: function (response) {
                $('#password_change_form').trigger('reset')
                $('#error_message').hide()
                $('#success_message').html(response.success_message)
                $('#success_message').show()
                $('#change_password_pop_up').modal('show')
            },
            error: function (error) {
                try {
                    $('#error_message').html(error.responseJSON.error_message)
                    $('#success_message').hide()
                    $('#error_message').show()
                    $('#change_password_pop_up').modal('show')
                } catch (error) {
                    console.error('Internal server down')
                }
            }
        })
    });