var clients_data = new Array();
var validate_add_attributes = [];
var client={};
var main_table_low_value = [];

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#upload_client_Modal').modal('show');
    new_row_data(); // Function for add a new row data
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

//**********************************************************
function onclick_copy_update_button() {
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
    for (var i = 0; i < $chkbox_all.length; i++) {
        if ($chkbox_all[i].checked) {
            var row = $chkbox_all[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
               unique_input = '<input class="form-control check_special_char" type="text" value="' + row.cells[1].innerHTML + '" name="client code"  maxlength="8" style="text-transform:uppercase" disabled>'
               edit_basic_data += '<tr ><td hidden><input type="checkbox" required></td><td><input class="form-control check_special_char" type="text" value="' + row.cells[1].innerHTML + '" name="client code"  maxlength="4" style="text-transform:uppercase" disabled></td><td><input class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" type="text"  name="description"  maxlength="30"  required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
               $("#header_select").prop("hidden", true);
            }
            else{
               unique_input = '<input class="form-control check_special_char" type="text" value="' + row.cells[1].innerHTML + '" name="client code"  maxlength="8" style="text-transform:uppercase" required>'
               edit_basic_data += '<tr><td ><input type="checkbox" required></td>'+
               '<td>'+unique_input+'</td>'+
               '<td><input class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" type="text"  name="description"  maxlength="30"  required></td>'+
               '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
               $("#header_select").prop("hidden", false);
            }
        }
    }
    $('#id_popup_tbody').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#upload_client_Modal').modal('show');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#upload_client_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_client").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_client_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
       $("#id_error_msg").html("");
    });
    new_row_data(); // Function for add a new row data
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_client_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_client_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.client + '</td><td>' + item.description + '</td></tr>';
    });
    $('#id_client_tbody').append(edit_basic_data);
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
    $('#upload_client_Modal').modal('hide');
    clients_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    clients_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        client={};
        client.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        client.client = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        client.description = row.find("TD").eq(2).find('input[type="text"]').val();
        if (client == undefined){
            client.client = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        validate_add_attributes.push(client.client);
        clients_data.push(client);
        table_sort_filter('id_popup_table');
    });
    return clients_data;
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.client = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.client);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var client_arr_obj = {};
        client_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(client_arr_obj.del_ind){
            client_arr_obj.client = row.find("TD").eq(1).html();
            client_arr_obj.description = row.find("TD").eq(2).html();
            main_table_client_checked.push(client_arr_obj);
        }
    });
}

//*******************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    var errorElement = document.getElementById("error_message");
    if (errorElement) {
        errorElement.textContent = error_message;
        errorElement.style.color = "Red";
    }
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#upload_client_Modal').modal('show');
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="form-control check_special_char" type="text" minlength="3" maxlength="8"  name="client"  required></td><td><input class="form-control check_special_char" type="text" maxlength="30"  name="description" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}