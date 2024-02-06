var uom_data = new Array();
var validate_add_attributes = [];
var uom={};
var main_table_low_value = [];

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "uom_upload"
    $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

   // onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
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

//onclick of add button display uomModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#uomModal').modal('show');
    new_row_data();  // Add a new row in popup
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//******************************************************
function onclick_copy_update_button(data) {
    $("#error_msg_id").css("display", "none")
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    //Reference the Table
    var res = get_all_checkboxes(); // Function to get all the checkboxes
    var $chkbox_all = $('td input[type="checkbox"]', res);
    //Reference the CheckBoxes in Table.
    var edit_basic_data = "";
    var unique_input = '';
    //Loop through the CheckBoxes.
    for (var i = 0; i < $chkbox_all.length; i++) {
        if ($chkbox_all[i].checked) {
            var row = $chkbox_all[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
                unique_input = '<input class="form-control check_character_no_space" type="text" value="' + row.cells[1].innerHTML + '" name="uom_id"  maxlength="2" style="text-transform:uppercase" disabled>'
                 edit_basic_data += '<tr><td hidden><input type="checkbox" required></td><td><input class="form-control check_character_no_space" type="text" value="' + row.cells[1].innerHTML + '" name="uom_id"  maxlength="3" style="text-transform:uppercase" disabled></td><td><input class="form-control check_special_character" value="' + row.cells[2].innerHTML + '" type="text"  name="uomdescription"  maxlength="100" style="text-transform:uppercase;" required></td><td><input class="form-control check_special_character" value="' + row.cells[3].innerHTML + '" type="text"  name="isocodeid"  maxlength="15" style="text-transform:uppercase" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                  $("#header_select").prop("hidden", true);
            }
            else{
                unique_input = '<input class="form-control check_character_no_space" type="text" value="' + row.cells[1].innerHTML + '" name="uom_id"  maxlength="2" style="text-transform:uppercase" required>'
                 edit_basic_data += '<tr><td><input type="checkbox" required></td><td><input class="form-control check_character_no_space" type="text" value="' + row.cells[1].innerHTML + '" name="uom_id"  maxlength="3" style="text-transform:uppercase" required></td><td><input class="form-control check_special_character" value="' + row.cells[2].innerHTML + '" type="text"  name="uomdescription"  maxlength="100"  style="text-transform:uppercase;" required></td><td><input class="form-control check_special_character" value="' + row.cells[3].innerHTML + '" type="text"  name="isocodeid"  maxlength="3" style="text-transform:uppercase" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                  $("#header_select").prop("hidden", false);
            }
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#uomModal').modal('show');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#uomModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_uom_code").prop("hidden", true);
    $("#id_error_msg_uom_name").prop("hidden", true);
    $("#id_error_msg_uom_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();


});

//**************************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#uomModal').modal('show');
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
 $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("");
    });
    if (GLOBAL_ACTION == "uom_upload") {
        basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="form-control check_character_no_space" type="text"  title="Minimum length is 1" minlength="1" maxlength="3"  name="uomcode" style="text-transform:uppercase;" required></td><td><input class="form-control check_special_character" type="text" maxlength="100"  name="uomdescription" style="text-transform:uppercase;" required></td><td><input class="form-control check_special_character" type="text" title="Minimum length is 1"  minlength="1" maxlength="3"  name="isocodeid"  style="text-transform:uppercase;" required></td><td class="class_del_checkbox"><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
        table_sort_filter('id_popup_table');
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
    }
    else{
    new_row_data();  // Add a new row in popup
    }
}

//**************************************
function update_check_message(messages) {
     $.each(messages, function (i, message) {
        $("#id_check_success_messages").append('<p>' + message + '</p>')
     });
    $("#id_check_success_messages").prop("hidden",false)
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_uom_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_uom_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.uom_id + '</td><td>' + item.uom_description + '</td><td>' + item.iso_code_id + '</td></tr>';
    });
    $('#id_uom_tbody').append(edit_basic_data);
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
    var uom_id_check = new Array();
    var main_table_low_value = new Array();
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        // Read data from the pop-up
        uom_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        uom_description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        iso_code_id = row.find("TD").eq(3).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');

        if (checked_box) {
            del_ind = '1';
        } else {
            del_ind = '0';

            // Check if uom_id, uom_description, and iso_code_id are not empty
            if (
                uom_id.trim() !== '' &&
                uom_description.trim() !== ''
            ) {
                if (uom_id_check.includes(uom_id)) {
                    $(row).remove();
                }
                uom_id_check.push(uom_id);

                main_table_low_value = get_main_table_data_upload(); // Read data from the main table
                if (main_table_low_value.includes(uom_id)) {
                    $(row).remove();
                }
                main_table_low_value.push(uom_id);
            }
        }
    });
    table_sort_filter_popup_pagination('id_popup_table');
    check_data();
}



// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#uomModal').modal('hide');
    uom_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data(){
    $('#id_popup_table').DataTable().destroy();
    uom_data = new Array();
    validate_add_attributes = [];
   $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        uom={};
        uom.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        uom.iso_code_id = row.find("TD").eq(3).find('input[type="text"]').val().toUpperCase();
        uom.uom_description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        uom.uom_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        if (uom == undefined){
        uom.uom_id = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        validate_add_attributes.push(uom.uom_id);
        uom_data.push(uom);
    });
    $('#id_popup_table').DataTable().destroy();
   return uom_data;
}

function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.uom_id = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.uom_id);
    });
    table_sort_filter('display_basic_table');
}

// Function to get main table data
function get_main_table_data_upload() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.uom_id = row.find("TD").eq(1).html();
        main_attribute.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        var compare = main_attribute.uom_id
        main_table_low_value.push(compare);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}

function get_selected_data(){
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var uom_arr_obj = {};
        uom_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(uom_arr_obj.del_ind){
            uom_arr_obj.uom_id = row.find("TD").eq(1).html();
            uom_arr_obj.uom_description = row.find("TD").eq(2).html();
            uom_arr_obj.iso_code_id = row.find("TD").eq(3).html();
            main_table_uom_checked.push(uom_arr_obj);
        }
    });
}

//Get message for check data function
function get_msg_desc_check_data(msg){
     var msg_type ;
     msg_type = message_config_details(msg);
     $("#error_msg_id").prop("hidden", false);
     return msg_type.messages_id_desc;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="form-control check_character_no_space" type="text"  title="Minimum length is 1" minlength="1" maxlength="3"  name="uomcode" style="text-transform:uppercase;" required></td><td><input class="form-control check_special_character" type="text" maxlength="100"  name="uomdescription"  style="text-transform:uppercase;" required></td><td><input class="form-control check_special_character" type="text" title="Minimum length is 1"  minlength="1" maxlength="3"  name="isocodeid"  style="text-transform:uppercase;" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}