var auth_group_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var auth_group={};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#auth_group_Modal').modal('hide');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#auth_group_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_auth_group_code").prop("hidden", true);
    $("#id_error_msg_auth_group_name").prop("hidden", true);
    $("#id_error_msg_auth_group_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_auth_group_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_auth_group_data, function(i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.auth_obj_grp + '</td><td>' + item.auth_grp_desc + '</td><td>' + item.auth_level + '</td><td>' + item.auth_obj_id + '</td><td hidden>' + item.auth_grp_guid + '</td></tr>';
    });
    $('#id_auth_group_tbody').append(edit_basic_data);
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

//**********************************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var auth_group_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        auth_obj_grp = row.find("TD").eq(1).find("select option:selected").val();
        auth_obj_id = row.find("TD").eq(4).find("select option:selected").val();
        auth_grp_desc = row.find("TD").eq(2).find("select option:selected").val().toUpperCase();
        auth_level = row.find("TD").eq(3).find("select option:selected").val();
        var compare = auth_obj_grp+'-'+auth_grp_desc+'-'+auth_obj_id+'-'+auth_level
        if (auth_group_code_check.includes(compare)) {
            $(row).remove();
        }
        auth_group_code_check.push(compare);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

//**********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#auth_group_Modal').modal('show');
}

// Onclick of save button in popup
$('#save_id').click(function () {
    $('#auth_group_Modal').modal('hide');
    auth_group_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    auth_group_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        auth_group = {};
        auth_group.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        auth_group.auth_obj_grp = row.find("TD").eq(1).find('select[type="text"]').val();
        auth_group.auth_grp_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        auth_group.auth_level = row.find("TD").eq(3).find("select option:selected").val();
        auth_group.auth_obj_id = row.find("TD").eq(4).find("select option:selected").val();
        auth_group.auth_grp_guid = row.find("TD").eq(5).find('input[type="text"]').val();
         if (auth_group == undefined) {
             auth_group.auth_obj_grp = row.find("TD").eq(1).find('input[type="text"]').val();
         }
        if (auth_group.auth_grp_guid == undefined) {
            auth_group.auth_grp_guid = ''
        }
        var compare = auth_group.auth_obj_grp + ' - ' + auth_group.auth_grp_desc + ' - ' + auth_group.auth_level+ ' - ' + auth_group.auth_obj_id
        validate_add_attributes.push(compare);
        auth_group_data.push(auth_group);
    });
    $('#id_popup_table').DataTable().destroy();
    return auth_group_data;
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.auth_obj_grp = row.find("TD").eq(1).html();
        main_attribute.auth_grp_desc = row.find("TD").eq(2).html().toUpperCase();
        main_attribute.auth_level = row.find("TD").eq(3).html();
        main_attribute.auth_obj_id = row.find("TD").eq(4).html();
        var main_attribute_compare = main_attribute.auth_obj_grp + ' - ' + main_attribute.auth_grp_desc + ' - ' + main_attribute.auth_level + ' - ' + main_attribute.auth_obj_id
        main_table_low_value.push(main_attribute_compare);
    });
    table_sort_filter('display_basic_table');
}

function get_auth_grp_data() {
    main_table_data = {}; // Object to store node values for each node type
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.auth_obj_grp = row.find("TD").eq(1).html();
        main_attribute.auth_grp_desc = row.find("TD").eq(2).html();
        main_attribute.auth_level = row.find("TD").eq(3).html().toUpperCase();
        main_attribute.auth_obj_id = row.find("TD").eq(4).html();
        var main_attribute_compare = main_attribute.auth_obj_grp + ' - ' + main_attribute.auth_grp_desc + ' - ' + main_attribute.auth_level + ' - ' + main_attribute.auth_obj_id
        if (!main_table_data.hasOwnProperty(main_attribute.auth_obj_grp)) {
            main_table_data[main_attribute.auth_obj_grp] = [];
        }
        main_table_data[main_attribute.auth_obj_grp].push({
            auth_level: main_attribute.auth_level,
            auth_obj_id: main_attribute.auth_obj_id
        });
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_auth_group_checked = []; // Clear the previous data before collecting new data
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var auth_group_arr_obj = {};
        auth_group_arr_obj.del_ind = checkbox.is(':checked');
        if( auth_group_arr_obj.del_ind) {
            auth_group_arr_obj.auth_obj_grp = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            auth_group_arr_obj.auth_grp_desc =  row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            auth_group_arr_obj.auth_level = row.find("TD").eq(3).find(".form-control").val() || row.find("TD").eq(3).html();
            auth_group_arr_obj.auth_obj_id = row.find("TD").eq(4).find(".form-control").val() || row.find("TD").eq(4).html();
            auth_group_arr_obj.auth_grp_guid = row.find("TD").eq(5).find('input[type="text"]').val() || row.find("TD").eq(5).html();
            main_table_auth_group_checked.push(auth_group_arr_obj);
        }
    });
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="input form-control authgroup" onchange="get_auth_level_values(this)">'+ auth_group_id_dropdown+'</select></td>'+
    '<td><input class="form-control description" type="text"  name="description" value="'+auth_grp_desc+'"  disabled></td>'+
    '<td><select class="form-control" id="authLevelDropdown" onchange="get_auth_obj_value(this)">'+auth_level_dropdown+'</select></td>'+
    '<td><select class="form-control">'+auth_obj_id_dropdown+'</select></td>'+
    '<td hidden><input type="text" value="GUID"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

function get_auth_level_values(selectElement) {
    var selected_auth_group = selectElement.value;
    for (var i = 0; i < rendered_auth_group_field_data.length; i++) {
        if (rendered_auth_group_field_data[i].field_type_id === selected_auth_group) {
            auth_grp_desc = rendered_auth_group_field_data[i].field_type_desc;
            break; // Exit the loop once a match is found
        }
    }
    $(selectElement).closest('tr').find('.description').val(auth_grp_desc);

    var authValues = main_table_data[selected_auth_group];
    main_table_auth_level = {};
    authValues.forEach(item => {
        var authLevel = item.auth_level; // Assuming this property holds the auth_level
        if (!main_table_auth_level[authLevel]) {
            main_table_auth_level[authLevel] = new Set();
        }
        main_table_auth_level[authLevel].add(item.auth_obj_id);
    });

    rendered_auth_level = {};
    rendered_auth_obj_data.forEach(item => {
        var authLevel = item.auth_level;
        if (!rendered_auth_level[authLevel]) {
            rendered_auth_level[authLevel] = new Set();
        }
        rendered_auth_level[authLevel].add(item.auth_obj_id);
    });

    var auth_levelDropdown = $(selectElement).closest('tr').find('.form-control').eq(2);
    auth_levelDropdown.empty();
    hiddenAuthLevelIDs = [];
    for (const authLevel in rendered_auth_level) {
        if (main_table_auth_level.hasOwnProperty(authLevel)) {
            if (rendered_auth_level[authLevel].size === main_table_auth_level[authLevel].size) {
                hiddenAuthLevelIDs.push(authLevel);
            } else {
                auth_levelDropdown.append('<option value="' + authLevel + '">' + authLevel + '</option>');
            }
        }
    }

    hiddenAuthObjectIDs = [];
    var options = auth_level_dropdown.split('<option value="');
    var firstAuthLevel = options[1].split('">')[0];
    const authLevel = firstAuthLevel;
    var auth_objDropdown = $(selectElement).closest('tr').find('.form-control').eq(3);
    auth_objDropdown.empty();
    if (rendered_auth_level[authLevel]) {
        rendered_auth_level[authLevel].forEach((auth_obj_id) => {
            if (main_table_auth_level[authLevel] && main_table_auth_level[authLevel].has(auth_obj_id)) {
                hiddenAuthObjectIDs.push(auth_obj_id);
            } else {
                auth_objDropdown.append('<option value="' + auth_obj_id + '">' + auth_obj_id + '</option>');
            }
        });
    }
}

function get_auth_obj_value(selectElement) {
    var selected_authLevel = $(selectElement).val();
    var authGroup_id = $(selectElement).closest('tr').find('.form-control').eq(0).val();
    var auth_objDropdown = $(selectElement).closest('tr').find('.form-control').eq(3);
    auth_objDropdown.empty();

    var authValues = main_table_data[authGroup_id];
    main_table_auth_level = {};
    authValues.forEach(item => {
        var authLevel = item.auth_level; // Assuming this property holds the auth_level
        if (!main_table_auth_level[authLevel]) {
            main_table_auth_level[authLevel] = new Set();
        }
        main_table_auth_level[authLevel].add(item.auth_obj_id);
    });

    if (rendered_auth_level[selected_authLevel]) {
        rendered_auth_level[selected_authLevel].forEach((auth_obj_id) => {
            if (main_table_auth_level[selected_authLevel] && main_table_auth_level[selected_authLevel].has(auth_obj_id)) {
                hiddenAuthObjectIDs.push(auth_obj_id);
            } else {
                auth_objDropdown.append('<option value="' + auth_obj_id + '">' + auth_obj_id + '</option>');
            }
        });
    }
}