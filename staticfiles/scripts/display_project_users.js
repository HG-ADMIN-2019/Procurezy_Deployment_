$(document).ready(function(){
    $("#supplier_form_reset").click(function(){
        $('#configform')[0].reset();
        $('#myModal').modal('hide');
    });

    $('#nav_menu_items').remove();
    $("body").css("padding-top", "4rem");
});

// Function to make user basic data field editable
//function edit_user_basic_info() {
//    $('#user_basic_update_success').hide();
//    $(".hg_edit_display_mode").prop("disabled", false);
//    $("#language_id").append(language_opt)
//    $("#currency_id").append(currency_opt)
//    $("#time_zone").append(timezone_opt)
//    $("#decimal_notation").append(decimal_opt)
//    $("#date_format").append(date_format_opt)
//    document.getElementById("edit_user_info_btn").style.display = "none"
//    document.getElementById("save_cancel_user_info_btn").style.display = "block"
//}

// Onlick cancel edit user-basic data
//function cancel_user_basic_info() {
//    $(".hg_edit_display_mode").prop("disabled", true);
//    document.getElementById("edit_user_info_btn").style.display = "block"
//    document.getElementById("save_cancel_user_info_btn").style.display = "none"
//}

    // Funtion to save basic detail data
    function save_proj_basic_info() {
     var project_id_val= $('#projectid').val();
     var project_name_val = $('project_name').val();
     var project_desc_val = $('#project_desc').val();
      is_save_form_valid = save_proj_form_validation(project_id_val, project_name_val, project_desc_val)
        if (is_save_form_valid != '') {
            $('#save_error_div').html(is_save_form_valid)
            $('#save_error_div').show()
            scroll_top()
            return
        }
        var proj_data_dict = {}

        proj_data_dict.username = $('#projectId').val();
        proj_data_dict.first_name = $('#project_name').val();
        proj_data_dict.last_name= $('#start date').val();
        proj_data_dict.employee_id= $('#project_id').val();
        proj_data_dict.user_type= $('#end date').val();
//        user_data_dict.language_id= $('#language_id').val();
//        user_data_dict.currency_id=$('#currency_id').val();
//        user_data_dict.time_zone= $('#time_zone').val();
//        user_data_dict.email= $('#email').val();
//        user_data_dict.phone_num= $('#phone_num').val();
//        user_data_dict.date_format= $('#date_format').val();
//        user_data_dict.decimal_notation= $('#decimal_notation').val();
//        user_data_dict.login_attempts= $('#login_attempts').val();
//        user_data_dict.super_user= $('#super_user').prop('checked');
//        user_data_dict.user_locke= $('#user_locked').prop('checked');
//        user_data_dict.pwd_locked= $('#pwd_locked').prop('checked');

        ajax_update_proj_basic_data(proj_data_dict)

        document.getElementById('proj_basic_update_success').innerHTML = response.message.message_desc;
          $('#save_error_div').hide()
        $('#user_basic_update_success').show();
        $('html, body').animate({ scrollTop: 0 }, 'slow');
        cancel_proj_basic_info();

    }
// Validation function
   const save_proj_form_validation = (project_id_val, project_name_val, project_desc_val) => {
        var is_valid = true
        var save_form_errors = ''
//        var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (project_id_val == '') {
            is_valid = false
             var msg = "JMSG007";
                            var msg_type ;
                          msg_type = message_config_details(msg);
                          $("#error_msg_id").prop("hidden", false)

                          if(msg_type.message_type == "ERROR"){
                                display_message("error_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "WARNING"){
                             display_message("id_warning_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "INFORMATION"){
                             display_message("id_info_msg_id", msg_type.messages_id_desc)
                          }

                           var display5 = msg_type.messages_id_desc;
            save_form_errors +=  display5 + "Project Id";
        }
        if (project_name_val == '') {
            is_valid = false
             var msg = "JMSG007";
                            var msg_type ;
                          msg_type = message_config_details(msg);
                          $("#error_msg_id").prop("hidden", false)

                          if(msg_type.message_type == "ERROR"){
                                display_message("error_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "WARNING"){
                             display_message("id_warning_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "INFORMATION"){
                             display_message("id_info_msg_id", msg_type.messages_id_desc)
                          }

                           var display6 = msg_type.messages_id_desc;
            save_form_errors += display6 + "Project name";
        }
        if (project_desc_val == '') {
            is_valid = false

                            var msg = "JMSG004";
                            var msg_type ;
                          msg_type = message_config_details(msg);
                          $("#error_msg_id").prop("hidden", false)

                          if(msg_type.message_type == "ERROR"){
                                display_message("error_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "WARNING"){
                             display_message("id_warning_msg_id", msg_type.messages_id_desc)
                          }
                          else if(msg_type.message_type == "INFORMATION"){
                             display_message("id_info_msg_id", msg_type.messages_id_desc)
                          }

                           var display8 = msg_type.messages_id_desc;
            save_form_errors += display8+ "project desc";
        }


        return is_valid, save_form_errors
    }
