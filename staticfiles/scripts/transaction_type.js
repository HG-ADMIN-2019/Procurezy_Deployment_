var transaction_types_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var TransactionTypes={};

// on click add icon display the row in to add the new entries
function add_popup_row() {
    dropdown_value();
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    eliminate_used_sequence()
    basic_add_new_html = '<tr><td><input class="checkbox_check" type="checkbox" required></td><td><input class="input form-control check_special_char" type="text" maxlength="15"  name="transaction type" style="text-transform:uppercase;" required></td><td><select class="input form-control" disabled>'+ document_type_dropdown +'</select></td><td><select type="text" id="id_sequence" class="input form-control">' + sequence_dropdown + '</select></td><td><input type="text" class="form-control check_special_char" maxlength="10"  name="transaction description"  required></td><td><input type="checkbox"  name="active_inactive" required></td><td hidden><input type="text" class= "form-control" name=" guid "></td><td hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "transaction_types_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup('id_popup_table');
}

//**********************************
function read_sequence() {
    rendered_sequence_array = [];
    sequence_remove_array = [];
    $.each(rendered_transaction_types_data, function (i, value) {
        sequence_remove_array.push(value.sequence)
    });

    $.each(rendered_sequence_num, function (i, item) {
        rendered_sequence_array.push(item.sequence)
    });
}

//*************************************

function eliminate_used_sequence() {
    read_sequence()
    sequence_dropdown = '';
    $.each(rendered_sequence_array, function (i, item) {
        if (sequence_remove_array.includes(item)) {
            rendered_sequence_array = $.grep(rendered_sequence_array, function (value) {
                return value != item;
            });
        }
    });
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        sequence_popup = row.find("TD").eq(3).find("select option:selected").val();
        rendered_sequence_array = $.grep(rendered_sequence_array, function (item) {
            return item != sequence_popup;
        });
    })
    $.each(rendered_sequence_array, function (i, value) {
        sequence_dropdown += '<option value="' + value + '">' + value + '</option>'
    });
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

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_transaction_types_code").prop("hidden", true);
    $("#id_error_msg_transaction_types_name").prop("hidden", true);
    $("#id_error_msg_transaction_types_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    // read_sequence();
    $('#id_popup_table').DataTable().destroy();
});

//****************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    transaction_types_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    transaction_types_data = new Array();
    validate_add_attributes = [];
    $('#myModal').modal('hide');
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        transaction_types = {};
        transaction_types.del_ind = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
        transaction_types.transaction_type = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        transaction_types.document_type = row.find("TD").eq(2).find("select option:selected").val();
        transaction_types.sequence = row.find("TD").eq(3).find('Select').val();
        transaction_types.description = row.find("TD").eq(4).find('input[type="text"]').val();
        transaction_types.active_inactive = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        transaction_types.guid = row.find("TD").eq(6).find('input[type="text"]').val();
        transaction_types.attribute_id ='FC_TRANS_TYPE'
        if (transaction_types == undefined) {
            transaction_types.transaction_type = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        }
        if (transaction_types.guid == undefined){
            transaction_types.guid = ''
        }
        var compare = transaction_types.transaction_type + '-' + transaction_types.document_type
        validate_add_attributes.push(compare);
        transaction_types_data.push(transaction_types);
    });
    table_sort_filter('id_popup_table');
    return transaction_types_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="input form-control check_special_char" type="text" maxlength="15"  name="transaction type" style="text-transform:uppercase;" required></td><td><select class="input form-control" disabled>'+ document_type_dropdown +'</select></td><td><select type="text" class="input form-control">' + sequence_dropdown + '</select></td><td><input type="text" class="form-control check_special_char" maxlength="10"  name="transaction description"  required></td><td><input type="checkbox"  name="active_inactive" required></td><td hidden><input type="text" class= "form-control" name=" guid "></td><td hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.transaction_type = row.find("TD").eq(1).html();
        main_attribute.document_type = row.find("TD").eq(2).html();
        main_attribute.sequence = row.find("TD").eq(3).html();
        main_attribute.description  = row.find("TD").eq(4).html();
        var compare_maintable = main_attribute.transaction_type + '-' + main_attribute.document_type
        main_table_low_value.push(compare_maintable);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var transaction_types_arr_obj = {};
        transaction_types_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if( transaction_types_arr_obj.del_ind){
            transaction_types_arr_obj.transaction_type = row.find("TD").eq(1).html();
            transaction_types_arr_obj.document_type = row.find("TD").eq(2).html();
            transaction_types_arr_obj.sequence = row.find("TD").eq(3).html();
            transaction_types_arr_obj.description = row.find("TD").eq(4).html();
            transaction_types_arr_obj.active_inactive = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            transaction_types_arr_obj.guid = row.find("TD").eq(6).html();
            main_table_transaction_types_checked.push(transaction_types_arr_obj);
        }
    });
}
