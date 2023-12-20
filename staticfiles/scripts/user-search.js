 // Script to generate sort and filter feature for tables
 $(document).ready( function() {
   nav_bar_admin();
   $("body").css("padding-top", "7rem");
   $('#username').val(localStorage.getItem("username"));
   $('#first_name').val(localStorage.getItem("first_name"));
   $('#last_name').val(localStorage.getItem("last_name"));
   $('#email').val(localStorage.getItem("email"));
   $('#user_type').val(localStorage.getItem("user_type"));
   $('#employee_id').val(localStorage.getItem("employee_id"));
   if(localStorage.getItem("user_locked") == "true"){
        $('#user_locked_id').prop("checked", true)
   }
   else{ $('#user_locked_id').prop("checked", false)}
   if(localStorage.getItem("pwd_locked") == "true"){
        $('#pwd_locked_id').prop("checked", true)
   }
   else{ $('#pwd_locked_id').prop("checked", false)}
   if(localStorage.getItem("is_active") == "true"){
        $('#is_active_id').prop("checked", true)
   }
   else{ $('#is_active_id').prop("checked", false)}
   const form = document.getElementById("search_form");
   table_sort_filter_basic("table_sort_filter_basic")
});

function validateForm(event) {
    var temp = $('#username').val();
    if($('#username').val() == ''){
        if($('#first_name').val() == ''){
            if($('#last_name').val() == ''){
                $('#error_message_search').text("Please enter Username or First name or Last name");
                document.getElementById("error_message_search").style.color = "Red";
                $("#error_msg").css("display", "block")
                CloseLoaderPopup();
                event.preventDefault();
                return false;
            }
        }
    }
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "employee_upload"
  //  $("#user_tab_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

// onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}

function display_file_select_error(){
    $("#id_error_msg_upload").prop("hidden",false);
    var msg = "JMSG110";
    var msg_type ;
    msg_type = message_config_details(msg);
    get_message_details(msg); // Get message details
    var display = msg_type.messages_id_desc;
    document.getElementById("id_error_msg_upload").innerHTML = display;
    document.getElementById("id_error_msg_upload").style.color = "Red";
    $('#id_data_upload').modal('show');
}
