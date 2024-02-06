var approval_limit_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var approval_limit={};

  // onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}


//**************************************
function approval_limit_find(company_num) {
    corresponding_values = {};
    corresponding_values.app_code_id_dropdown = '';
    corresponding_values.other_dropdn = '';
    company_list = company_list;
    unique_user_name= [];
    unique_app_code = [];
    for (var i = 0; i < company_list.length; i++) {
        compare_dict = {};
        compare_dict = company_list[i]
        if (company_num == compare_dict.company_id) {
            unique_app_code.push(compare_dict.app_code_id);
        }
    }
    for (var i = 0; i < arrDistinct.length; i++) {
        corresponding_values.other_dropdn += '<option value="'+arrDistinct[i]+'">' + arrDistinct[i] + '</option>'
    }
    appcodeDistinct = [];
    $(unique_app_code).each(function (index, item) {
        if ($.inArray(item, appcodeDistinct) == -1)
        appcodeDistinct.push(item);
    });
    for (var i = 0; i < appcodeDistinct.length; i++) {
        corresponding_values.app_code_id_dropdown += '<option value="'+appcodeDistinct[i]+'">' + appcodeDistinct[i] + '</option>'
    }
    return corresponding_values
}

//**********************************
function company_dropdwn_change(row){
    row.find("TD").eq(3).find("select").empty()
    company_num = row.find("TD").eq(1).find("select option:selected").val();
    var comp_val = approval_limit_find(company_num)
    row.find("TD").eq(3).find("select").append(comp_val.app_code_id_dropdown)
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "approval_limit_upload"
    $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
     $("#save_id").prop("hidden", false);
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#App_limt_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_approval_limit_code").prop("hidden", true);
    $("#id_error_msg_approval_limit_name").prop("hidden", true);
    $("#id_error_msg_approval_limit_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_approval_limit_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_approval_limit_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.company_id + '</td><td>' + item.approver_username + '</td><td>' + item.app_code_id + '</td><td hidden>' + item.app_guid + '</td></tr>';
    });
    $('#id_approval_limit_tbody').append(edit_basic_data);
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

//*****************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var approval_limit_code_check = new Array
    var main_table_low_value = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        aapprover_username = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        company_id = row.find("TD").eq(1).find("select option:selected").val();
        app_code_id = row.find("TD").eq(3).find("select option:selected").val();  
        app_guid = row.find("TD").eq(4).find('input[type="text"]').val().toUpperCase()
        approval_limit_compare = approver_username +'-'+ company_id +'-'+ app_code_id 
        if (approval_limit_code_check.includes(approval_limit_compare)) {
            $(row).remove();
        }
        approval_limit_code_check.push(approval_limit_compare);
        main_table_low_value = get_main_table_data_upload(); //Read data from main table
        if (main_table_low_value.includes(approval_limit_compare)) {
            $(row).remove();
        }
        main_table_low_value.push(approval_limit_compare);
        })
        table_sort_filter_popup_pagination('id_popup_table')
        check_data()
    }

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#App_limt_Modal').modal('hide');
    approval_limit_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    validate_add_attributes = [];
    var approval_limit_data = new Array();
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        approval_limit = {};
        approval_limit.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        approval_limit.approver_username = row.find("TD").eq(2).find("select option:selected").val();
        approval_limit.company_id = row.find("TD").eq(1).find("select option:selected").val();
        approval_limit.app_code_id = row.find("TD").eq(3).find("select option:selected").val();
        approval_limit.app_guid = row.find("TD").eq(4).find('input[type="text"]').val().toUpperCase()
        var approval_limit_compare = approval_limit.approver_username +'-'+ approval_limit.company_id +'-'+ approval_limit.app_code_id
        if (approval_limit == undefined) {
            approval_limit.approver_username = row.find("TD").eq(1).find("select option:selected").val();
        }
        if(approval_limit.app_guid == undefined) {
                approval_limit.app_guid = ''
            }
        validate_add_attributes.push(approval_limit_compare);
        approval_limit_data.push(approval_limit);
    });
    table_sort_filter('id_popup_table');
    return approval_limit_data;
}

function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#App_limt_Modal').modal('show');
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control" name="company_dropdown" type="text">'+company_id_dropdown+'</select></td><td><select class="form-control" type="text">'+user_name_dropdown+'</select></td><td><select class="form-control" type="text">'+app_code_id_dropdown+'</select></td><td hidden><input type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    var table = $('#id_popup_table').DataTable();
    table.row.add($(basic_add_new_html)).draw();
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.approver_username = row.find("TD").eq(2).html();
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.app_code_id = row.find("TD").eq(3).html();
        main_attribute.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        var approval_limit_compare_maintable = main_attribute.approver_username +'-'+main_attribute.company_id +'-'+ main_attribute.app_code_id
        main_table_low_value.push(approval_limit_compare_maintable);
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
        main_attribute.approver_username = row.find("TD").eq(2).html();
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.app_code_id = row.find("TD").eq(3).html();
        main_attribute.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        var approval_limit_compare_maintable = main_attribute.approver_username +'-'+main_attribute.company_id +'-'+ main_attribute.app_code_id+ '-'+ main_attribute.del_ind
        main_table_low_value.push(approval_limit_compare_maintable);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var approval_limit_arr_obj = {};
        approval_limit_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(approval_limit_arr_obj.del_ind){
        approval_limit_arr_obj.approver_username = row.find("TD").eq(2).html();
        approval_limit_arr_obj.company_id = row.find("TD").eq(1).html();
        approval_limit_arr_obj.app_code_id = row.find("TD").eq(3).html();
        approval_limit_arr_obj.app_guid = row.find("TD").eq(4).html();
        main_table_approval_limit_checked.push(approval_limit_arr_obj);
        }
    });
}