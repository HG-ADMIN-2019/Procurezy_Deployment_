var incoterms_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var incoterm = {};

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

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
//function onclick_upload_button() {
//    GLOBAL_ACTION = "incoterm_upload"
//    $("#id_popup_tbody").empty();
//    $('#id_data_upload').modal('show');
//}

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
    //Loop through the CheckBoxes.
    for (var i = 0; i < $chkbox_all.length; i++) {
       if ($chkbox_all[i].checked) {
            var row = $chkbox_all[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
               unique_input = '<input class="form-control" value = "'+ row.cells[1].innerHTML +'" name="incoterm_key" maxlength="3"  type="text" readonly>'
                 edit_basic_data += '<tr><td hidden><input type="checkbox"></td>'+
                 '<td>'+ unique_input +'</td>'+
                  '<td><input class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" name="description" maxlength="50" type="text" ></td>'+
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", true);
            }
            else {
                unique_input = '<input class="form-control check_special_char" value = "'+ row.cells[1].innerHTML +'" name="incoterm_key" maxlength="3" type="text" pattern="[A-Z]" style="text-transform:uppercase;">'
                edit_basic_data += '<tr><td><input type="checkbox" required></td>'+
                '<td>'+ unique_input +'</td>'+
                '<td><input class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" maxlength="50" name="description" type="text" ></td>'+
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
            }
        }
    }
    $('#id_popup_tbody').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#Incoterms_Modal').modal('show');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Incoterms_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_incoterm_key").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//onclick of add button display Incoterms_Modal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#Incoterms_Modal').modal('show');
    new_row_data();   // Add a new row in popup
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $("#header_select").prop("hidden", false);
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    new_row_data();   // Add a new row in popup
}

function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#Incoterms_Modal').modal('show');
 }

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_incoterm_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_incoterm_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.incoterm_key + '</td><td>' + item.description + '</td></tr>';
    });
    $('#id_incoterm_tbody').append(edit_basic_data);
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

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#Incoterms_Modal').modal('hide');
    incoterms_data =  read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    incoterms_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        incoterm = {};
        incoterm.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        incoterm.description = row.find("TD").eq(2).find('input[type="text"]').val();
        incoterm.incoterm_key = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        if (incoterm == undefined) {
            incoterm.incoterm_key = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        validate_add_attributes.push(incoterm.incoterm_key);
        incoterms_data.push(incoterm);
    });
    table_sort_filter('id_popup_table');
    return incoterms_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><input class="input form-control check_special_char" minlength="3" maxlength="3" name="incoterm_key" type="text" pattern="[A-Z]" style="text-transform:uppercase;" ></td>'+
    '<td><input  class="form-control check_special_char"  maxlength="50" name="description" type="text"></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.incoterm_key = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.incoterm_key);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var incoterm_arr_obj ={};
        incoterm_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(incoterm_arr_obj.del_ind) {
            incoterm_arr_obj.incoterm_key = row.find("TD").eq(1).html();
            incoterm_arr_obj.description = row.find("TD").eq(2).html();
            main_table_incoterm_checked.push(incoterm_arr_obj);
        }
    });
}


function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var incoterm_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        description = row.find("TD").eq(2).find('input[type="text"]').val();
        incoterm_key = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        if (incoterm_code_check.includes(incoterm_key)) {
            $(row).remove();
        }
//        validate_add_attributes.push(incoterm.incoterm_key);
        incoterm_code_check.push(incoterm_key);
    });
    table_sort_filter_popup_pagination('id_popup_table')
}

//Get message for check data function
function get_msg_desc_check_data(msg){
    var msg_type ;
    msg_type = message_config_details(msg);
    $("#error_msg_id").prop("hidden", false);
    return msg_type.messages_id_desc;
}