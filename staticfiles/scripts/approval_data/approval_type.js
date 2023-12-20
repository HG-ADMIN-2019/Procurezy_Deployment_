var approval_type_data = new Array();
var main_table_low_value = [];
var validate_add_attributes = [];

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#App_Type_Modal').modal('hide');
}

//******************************************** 
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block");
    $('#id_save_confirm_popup').modal('hide');
    $('#App_Type_Modal').modal('show');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#App_Type_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_approval_type_code").prop("hidden", true);
    $("#id_error_msg_approval_type_name").prop("hidden", true);
    $("#id_error_msg_approval_type_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

// Function for add a new row data
function new_row_data(inc_index) {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
        '<td><select type="text" class="input form-control approvaltype"  name="approvaltype" onchange="GetSelectedTextValue(this)">'+ approval_type_dropdown +'</select></td>'+
        '<td><input class="form-control description" type="text"  name="description"  value="'+desc_app_type+'" disabled></td>'+
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_approval_type_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_approval_type_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.app_types + '</td><td>' + item.appr_type_desc + '</td></tr>';
    });
    $('#id_approval_type_tbody').append(edit_basic_data);
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

//**********************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var approval_type_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        appr_type_desc = row.find("TD").eq(2).find('input[type="text"]').val();
        app_types = row.find("TD").eq(1).find('Select[type="text"]').val();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')
        if (approval_type_code_check.includes(app_types)) {
            $(row).remove();
        }
        approval_type_code_check.push(app_types);
    })
    table_sort_filter_popup('id_popup_table')
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#App_Type_Modal').modal('hide');
    approval_type_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    approval_type_data = new Array();
    validate_add_attributes = [];
    var approval_type = {};
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        approval_type = {};
        approval_type.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        approval_type.appr_type_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        approval_type.app_types = row.find("TD").eq(1).find('select[type="text"]').val();
        if (approval_type == undefined) {
            approval_type.app_types = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        validate_add_attributes.push(approval_type.app_types);
        approval_type_data.push(approval_type);
    });
    table_sort_filter('id_popup_table');
    return approval_type_data;
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.app_types = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.app_types);
    });
    table_sort_filter('display_basic_table');
}


// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var approval_type_arr_obj = {};
        approval_type_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(approval_type_arr_obj.del_ind){
        approval_type_arr_obj.app_types = row.find("TD").eq(1).html();
        approval_type_arr_obj.appr_type_desc = row.find("TD").eq(2).html();
        main_table_approval_type_checked.push(approval_type_arr_obj);
        }
    });
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_checked = [];
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var approval_type_arr_obj = {};
        approval_type_arr_obj.del_ind = checkbox.is(':checked');
        if(approval_type_arr_obj.del_ind) {
            approval_type_arr_obj.app_types = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            approval_type_arr_obj.appr_type_desc = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            main_table_checked.push(approval_type_arr_obj);
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
