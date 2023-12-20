var timezone_data = new Array();
var validate_add_attributes = [];
var timezone={};
var main_table_low_value = [];

//onclick of add button display timezoneModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#timezoneModal').modal('show');
    new_row_data();  // Add a new row in popup
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "timezone_upload"
    $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
     $("#save_id").prop("hidden", false);
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
     $("#save_id").prop("hidden", false);
}

//**********************************************************
function onclick_copy_update_button(data) {
    $("#error_msg_id").css("display", "none")
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    //Reference the Table.
    var res = get_all_checkboxes(); // Function to get all the checkboxes
    var $chkbox_all = $('td input[type="checkbox"]', res);
    //Reference the CheckBoxes in Table.
    var edit_basic_data = "";
    var unique_input = '';
    //Loop through the CheckBoxes.
    for (var i = 0; i <  $chkbox_all.length; i++) {
        if ( $chkbox_all[i].checked) {
            var row =  $chkbox_all[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
                unique_input = '<input class="form-control check_character_no_space" type="text" value="' + row.cells[1].innerHTML + '" name="time_zone"  maxlength="6" style="text-transform:uppercase" disabled>'
                edit_basic_data += '<tr><td hidden><input type="checkbox" required></td>'+
                 '<td>'+ unique_input +'</td>'+
                 '<td><input class="form-control check_special_character" value="' + row.cells[2].innerHTML + '" type="text"  name="description"  maxlength="255" style="text-transform:uppercase;" required></td>'+
                 '<td><input class="form-control check_UTC_Difference" value="' + row.cells[3].innerHTML + '" type="text"  name="utcdifference"  maxlength="15" style="text-transform:uppercase" required></td>'+
                 '<td><input class="form-control check_special_character" value="' + row.cells[4].innerHTML + '" type="text"  name="daylightsave"  maxlength="10" style="text-transform:uppercase"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", true);
            }
            else{
                unique_input = '<input class="form-control check_character_no_space" type="text" value="' + row.cells[1].innerHTML + '" name="time_zone"  maxlength="6" style="text-transform:uppercase" required>'
                edit_basic_data += '<tr><td><input type="checkbox" required></td>'+
                '<td>'+ unique_input +'</td>'+
                '<td><input class="form-control check_special_character" value="' + row.cells[2].innerHTML + '" type="text"  name="description"  maxlength="255" style="text-transform:uppercase;" required></td>'+
                '<td><input class="form-control check_UTC_Difference" value="' + row.cells[3].innerHTML + '" type="text"  name="utcdifference"  maxlength="15" style="text-transform:uppercase" required></td>'+
                '<td><input class="form-control check_special_character" value="' + row.cells[4].innerHTML + '" type="text"  name="daylightsave"  maxlength="10" style="text-transform:uppercase"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
            }
        }
    }
    $('#id_popup_tbody').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#timezoneModal').modal('show');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#timezoneModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_timezone_code").prop("hidden", true);
    $("#id_error_msg_timezone_name").prop("hidden", true);
    $("#id_error_msg_timezone_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true);
    $("#id_check_data").prop("hidden", true);
    $("#id_error_msg_upload").prop("hidden",true);
    $("#id_error_msg_upload").css("display", "none");
    $('#id_popup_table').DataTable().destroy();
});

function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#countriesModal').modal('show');
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("no records found");
    });
    if (GLOBAL_ACTION == "timezone_upload") {
            basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
        '<td><input class="input form-control check_character_no_space" type="text"  title="Minimum length is 3" minlength="1" maxlength="5"  name="timezonecode" style="text-transform:uppercase;" required></td>'+
        '<td><input class="input form-control check_special_character" type="text" maxlength="255"  name="timezonename" style="text-transform:uppercase;" required></td>'+
        '<td><input class="input form-control check_UTC_Difference" type="text" title="Minimum length is 15" minlength="15" maxlength="15"  name="utcdifference"  style="text-transform:uppercase;" required></td>'+
        '<td><input class="input form-control check_special_character" type="text" maxlength="10"  name="daylightsave"   style="text-transform:uppercase;" required></td><td class="class_del_checkbox"><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
        table_sort_filter('id_popup_table');
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
    else{
         new_row_data();   // Add a new row in popup
        table_sort_filter('id_popup_table');
    }
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_timezone_tbody').empty();
    var edit_basic_data = '';
  // get rendered data
    $.each(rendered_timezone_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.time_zone + '</td><td>' + item.description + '</td><td>' + item.utc_difference + '</td><td>' + item.daylight_save_rule + '</td></tr>';
    });
    $('#id_timezone_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    $('#id_check_all').hide(); 
    table_sort_filter('display_basic_table');
}


function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var time_zone_check = new Array();
    var main_table_low_value = new Array();
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        // Read data from the pop-up
        time_zone = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        utc_difference = row.find("TD").eq(3).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');

        if (checked_box) {
            del_ind = '1';
        } else {
            del_ind = '0';

            // Check if time_zone, description, and utc_difference are not empty
            if (time_zone && description) {

                if (time_zone_check.includes(time_zone)) {
                    $(row).remove();
                }
                time_zone_check.push(time_zone);

                main_table_low_value = get_main_table_data_upload(); // Read data from the main table
                if (main_table_low_value.includes(time_zone)) {
                    $(row).remove();
                }
                main_table_low_value.push(time_zone);
            }
        }
    });
    table_sort_filter_popup_pagination('id_popup_table');
    check_data();
}


// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#timezoneModal').modal('hide');
    timezone_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    $('#id_popup_table').DataTable().destroy();
    timezone_data = new Array();
    validate_add_attributes = [];
   $("#id_popup_table TBODY TR").each(function () {
           var row = $(this);
           timezone={};
           timezone.time_zone = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
           timezone.description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
           timezone.utc_difference = row.find("TD").eq(3).find('input[type="text"]').val().toUpperCase();
           timezone.daylight_save_rule = row.find("TD").eq(4).find('input[type="text"]').val().toUpperCase();
           timezone.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');

           if (timezone == undefined) {
                timezone.time_zone = row.find("TD").eq(1).find('input[type="text"]').val();
           }
           validate_add_attributes.push(timezone.time_zone);
           timezone_data.push(timezone);
       });
       table_sort_filter('id_popup_table');
       return timezone_data;
}

function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.time_zone = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.time_zone);
    });
    table_sort_filter('display_basic_table');
}


// onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}

// Function to get main table data
function get_main_table_data_upload() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.time_zone = row.find("TD").eq(1).html();
        main_attribute.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        var compare = main_attribute.time_zone
        main_table_low_value.push(compare);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}

function get_selected_data(){
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var timezone_arr_obj = {};
        timezone_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(timezone_arr_obj.del_ind){
        timezone_arr_obj.time_zone = row.find("TD").eq(1).html();
        timezone_arr_obj.description = row.find("TD").eq(2).html();
        timezone_arr_obj.utc_difference = row.find("TD").eq(3).html();
        timezone_arr_obj.daylight_save_rule = row.find("TD").eq(4).html();
        main_table_timezone_checked.push(timezone_arr_obj);
        }
    });
}
// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
    '<td><input class="input form-control check_character_no_space" type="text"  title="Minimum length is 3" minlength="3" maxlength="5"  name="timezonecode" style="text-transform:uppercase;" required></td>'+
    '<td><input class="input form-control check_special_character" type="text" maxlength="255"  name="timezonename" style="text-transform:uppercase;" required></td>'+
    '<td><input class="input form-control check_UTC_Difference" type="text" title="Minimum length is 15" minlength="15" maxlength="15"  name="utcdifference"  style="text-transform:uppercase;" required></td>'+
    '<td><input class="input form-control check_special_character" type="text" maxlength="10"  name="daylightsave"   style="text-transform:uppercase;" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
}

//Get message for check data function
function get_msg_desc_check_data(msg){
     var msg_type ;
     msg_type = message_config_details(msg);
     $("#error_msg_id").prop("hidden", false);
     return msg_type.messages_id_desc;
}

//**************************************
function update_check_message(messages) {
     $.each(messages, function (i, message) {
        $("#id_check_success_messages").append('<p>' + message + '</p>')
     });
    $("#id_check_success_messages").prop("hidden",false)
}
