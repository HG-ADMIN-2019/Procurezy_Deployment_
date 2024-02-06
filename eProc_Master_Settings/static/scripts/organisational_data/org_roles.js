var roles_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var roles={};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#Roles_Modal').modal('hide');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Roles_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_roles_code").prop("hidden", true);
    $("#id_error_msg_roles_name").prop("hidden", true);
    $("#id_error_msg_roles_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_roles_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_roles_data, function (i, item) {
     edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.role + '</td><td>' + item.role_desc + '</td></tr>';
    });
    $('#id_roles_tbody').append(edit_basic_data);
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

//*********************************************
function display_error_message(error_message) {
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#Roles_Modal').modal('show');
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#Roles_Modal').modal('hide');
    roles_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    roles_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        roles = {};
        roles.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        roles.role = row.find("TD").eq(1).find('select[type="text"]').val();
        roles.role_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        if (roles == undefined) {
            roles.role = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        validate_add_attributes.push(roles.role);
        roles_data.push(roles);
    });
    table_sort_filter('id_popup_table');
    return roles_data;
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html='<tr><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="input form-control roles"  name="role" onchange="GetSelectedTextValue(this)">'+ roles_type_dropdown +'</select></td>'+
    '<td><input class="form-control description" type="text"  name="role_desc" value="'+roles_desc+'" disabled></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    var rolesSelect = $("#roles-1");
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.role = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.role);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_roles_checked = [];
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var roles_arr_obj = {};
        roles_arr_obj.del_ind = checkbox.is(':checked');
        if(roles_arr_obj.del_ind) {
            roles_arr_obj.role = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            roles_arr_obj.role_desc = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            main_table_roles_checked.push(roles_arr_obj);
        }
    });
}