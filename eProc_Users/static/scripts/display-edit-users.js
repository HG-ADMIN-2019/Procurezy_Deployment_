var sup_user = '';

// Function to make user basic data field editable
function edit_user_basic_info() {
    $('#user_basic_update_success').hide();
    $(".hg_edit_display_mode").prop("disabled", false);
    if(GLOBAL_ACTION != 'CREATE'){
        $('#username').prop("disabled", true);
        $('#employee_id').prop("disabled", true);
        $('#user_type').prop("disabled", true);
        $('#email').prop("disabled", true);
        $('#login_attempts').prop("disabled", true);
        $("#cancel_button").prop("hidden", false);
        $("#save_user_info_btn").prop("hidden", false);
    }
    document.getElementById("edit_user_info_btn").style.display = "none";
    document.getElementById("save_user_info_btn").style.display = "block";
    document.getElementById("cancel_button").style.display = "block";
    sup_user = document.getElementById("is_superuser").value;
    user_status = document.getElementById("user_status").value;
    user_locked = document.getElementById("user_locked").value;
    pwd_locked = document.getElementById("pwd_locked").value;
    set_value();
}

// Onlick cancel edit user-basic data 
function cancel_user_basic_info() {
    $(".hg_edit_display_mode").prop("disabled", true);
    document.getElementById("edit_user_info_btn").style.display = "block"
    document.getElementById("save_user_info_btn").style.display = "none";
    document.getElementById("cancel_button").style.display = "none";
    $(".error_message").prop("hidden", true);
    get_values();
}

function check(){
    $(".hg_edit_display_mode").prop("disabled", true);
    document.getElementById("edit_user_info_btn").style.display = "block"
    document.getElementById("save_user_info_btn").style.display = "none";
    document.getElementById("cancel_button").style.display = "none";
    $(".error_message").prop("hidden", true);
}

function set_value(){
     localStorage.setItem("username", document.getElementById("username").value);
     localStorage.setItem("employee_id", document.getElementById("employee_id").value);
     localStorage.setItem("user_type", document.getElementById("user_type").value);
     localStorage.setItem("first_name", document.getElementById("first_name").value);
     localStorage.setItem("last_name", document.getElementById("last_name").value);
     localStorage.setItem("email", document.getElementById("email").value);
     localStorage.setItem("phone_num", document.getElementById("phone_num").value);
     localStorage.setItem("date_format", document.getElementById("date_format").value);
     localStorage.setItem("decimal_notation", document.getElementById("decimal_notation").value);
     localStorage.setItem("is_superuser", document.getElementById("is_superuser").value);
     localStorage.setItem("user_status", document.getElementById("user_status").value);
     localStorage.setItem("user_locked", document.getElementById("user_locked").value);
     localStorage.setItem("pwd_locked", document.getElementById("pwd_locked").value);
     localStorage.setItem("currency_id", document.getElementById("id_currency_id").value);
     localStorage.setItem("language_id", document.getElementById("id_language_id").value);
     localStorage.setItem("time_zone", document.getElementById("id_time_zone").value);
}
function get_values(){
     $('#username').val(localStorage.getItem("username"));
     $('#employee_id').val(localStorage.getItem("employee_id"));
     $('#user_type').val(localStorage.getItem("user_type"));
     $('#first_name').val(localStorage.getItem("first_name"));
     $('#last_name').val(localStorage.getItem("last_name"));
     $('#email').val(localStorage.getItem("email"));
     $('#phone_num').val(localStorage.getItem("phone_num"));
     $('#date_format').val(localStorage.getItem("date_format"));
     $('#decimal_notation').val(localStorage.getItem("decimal_notation"));
     if(sup_user == "1"){
//        $('#is_superuser').val(1);
        $("#is_superuser").prop("checked", true)
     }
     else{
//        $('#is_superuser').val(0);
        $("#is_superuser").prop("checked", false)
    }
    if(user_status == "1"){
        $("#user_status").prop("checked", true)
    }
    else{
        $("#user_status").prop("checked", false)
    }
    if(user_locked == "1"){ $("#user_locked").prop("checked", true) }
    else{ $("#user_locked").prop("checked", false) }
    if(pwd_locked == "1"){ $("#pwd_locked").prop("checked", true) }
    else{ $("#pwd_locked").prop("checked", false) }
//     $('#user_status').val(localStorage.getItem("user_status"));
//     $('#user_locked').val(localStorage.getItem("user_status"));
//     $('#pwd_locked').val(localStorage.getItem("pwd_locked"));
   $('#id_currency_id').val(localStorage.getItem("currency_id"));
   $('#id_language_id').val(localStorage.getItem("language_id"));
   $('#id_time_zone').val(localStorage.getItem("time_zone"));
}


// Validation function
function save_user_form_validation(){
   var is_valid = true;
        var save_form_errors = ''
        var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

        var err_text1 = '';
        var temp = document.getElementsByClassName('mandatory_fields');
        for (var i = 0; i<temp.length; i++) {
            if(temp[i].nodeName == "SELECT"){
                if((temp[i].value == '') || (temp[i].value == null)){
                    err_text1 = temp[i].parentNode.children[0].innerHTML;
                    var display_id = temp[i].nextElementSibling.id;
                    $('#'+display_id).prop('hidden', false);
                    $('#temp[i].nextElementSibling.id').html("required");
                    document.getElementById(temp[i].nextElementSibling.id).innerHTML = err_text1 + " required";
                    is_valid = false;
                }
                else{ $('#temp[i].nextElementSibling.id').prop('hidden', true);
                }
            }
            else if(temp[i].nodeName == "INPUT"){
                var data = temp[i].value;
                var count = data.split('**').length - 1;
                if((temp[i].value == '') || (temp[i].value.indexOf("  ") >= 0)){
                    var err_text = temp[i].parentNode.children[0].innerHTML;
                    $(".error_message").prop("hidden", false);
                    temp[i].nextElementSibling.innerHTML = err_text + " required";
                   is_valid = false;
                }
                else if((count >= 1) || (data.includes('*'))){
                    var err_text = temp[i].parentNode.children[0].innerHTML;
                    $(".error_message").prop("hidden", false);
                    var display_id = temp[i].nextElementSibling.id;
                    $('#'+display_id).prop('hidden', false);
                    document.getElementById(display_id).style.display = "block";
                    temp[i].nextElementSibling.innerHTML = "Please enter valid value";
                   is_valid = false;
                }
                 else if((temp[i].value.length < 3) || ((count >= 1) || (data == '*'))){
                    var err_text = temp[i].parentNode.children[0].innerHTML;
                    $(".error_message").prop("hidden", false);
                    var display_id = temp[i].nextElementSibling.id;
                    $('#'+display_id).prop('hidden', false);
                    document.getElementById(display_id).style.display = "block";
                    temp[i].nextElementSibling.innerHTML = "Please enter min 3 chars for "+ err_text;
                    $('#'+temp[i].id).prop("disabled", false);
                   is_valid = false;
                }
                if(temp[i].id == 'email'){
                    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                     if (!(temp[i].value).match(mailformat)) {
                            valid_data = false
                             var msg = "JMSG002";
                             var msg_type ;
                             msg_type = message_config_details(msg);
                             var display1 = msg_type.messages_id_desc;
                             $(".error_message").prop("hidden", false);
                            var display_id = temp[i].nextElementSibling.id;
                            $('#'+display_id).prop('hidden', false);
                            document.getElementById(display_id).style.display = "block";
                            temp[i].nextElementSibling.innerHTML = display1 + " for Email Id";
                           is_valid = false;
                     }
                }
                if((temp[i].id == 'phone_num') || (temp[i].value.indexOf(" ") >= 0)) {
                     if (temp[i].value.length != 10) {
                            valid_data = false
                             var msg = "JMSG002";
                             var msg_type ;
                             msg_type = message_config_details(msg);
                             var display1 = msg_type.messages_id_desc;
                             $(".error_message").prop("hidden", false);
                            var display_id = temp[i].nextElementSibling.id;
                            $('#'+display_id).prop('hidden', false);
                            document.getElementById(display_id).style.display = "block";
                            temp[i].nextElementSibling.innerHTML = display1 + "";
                           is_valid = false;
                     }
                }
            }
        }
        return is_valid
    }

