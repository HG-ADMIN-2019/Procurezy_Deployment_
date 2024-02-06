var wfacc_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var wfacc = {};

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "workflowacc_upload"
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

//*********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block");
    $('#id_save_confirm_popup').modal('hide');
    $('#Wf_Acc_Modal').modal('show');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Wf_Acc_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_wfacc").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#Wf_Acc_Modal').modal('hide');
    wfacc_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    wfacc_data = new Array();
    validate_add_attributes = [];
    var wfacc = {};
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        wfacc = {};
        wfacc.del_ind = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
        wfacc.company_id = row.find("TD").eq(1).find('select[type="text"]').val();
        wfacc.account_assign_cat = row.find("TD").eq(2).find('select[type="text"]').val();
        wfacc.acc_value = row.find("TD").eq(3).find('select[type="text"]').val();
        wfacc.app_username = row.find("TD").eq(4).find('select[type="text"]').val();
        wfacc.sup_company_id = row.find("TD").eq(5).find('select[type="text"]').val();
        wfacc.sup_account_assign_cat = row.find("TD").eq(6).find('select[type="text"]').val();
        wfacc.sup_acc_value = row.find("TD").eq(7).find('select[type="text"]').val();
        wfacc.sup_currency_id = row.find("TD").eq(8).find('select[type="text"]').val();
        wfacc.workflow_acc_guid = row.find("TD").eq(9).find('input[type="text"]').val();
        if (wfacc == undefined) {
            wfacc.app_username = row.find("TD").eq(4).find('select[type="text"]').val();
        }
        if(wfacc.workflow_acc_guid == undefined) {
            wfacc.workflow_acc_guid = ''
        }
        var wfacc_compare = wfacc.company_id +'-'+  wfacc.account_assign_cat +'-'+ wfacc.acc_value +'-'+ wfacc.app_username +'-'+ wfacc.sup_company_id +'-'+wfacc.sup_account_assign_cat +'-'+ wfacc.sup_acc_value +'-'+ wfacc.sup_currency_id
        validate_add_attributes.push(wfacc_compare);
        wfacc_data.push(wfacc);
    });
    table_sort_filter('id_popup_table');
    return wfacc_data;
}

// Function for add a new row data
function new_row_data()  {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="form-control">'+ company_id_dropdown +'</select></td>'+
    '<td><select type="text" class="form-control">'+ acc_ass_dropdwn+'</select></td>'+
    '<td><select type="text" class="form-control">'+acc_ass_val_dropdwn+'</select></td>'+
    '<td><select type="text" class="form-control">'+ user_dropdwn +'</select></td>'+
    '<td><select type="text" class="form-control">'+ supcompany_dropdwn +'</select></td>'+
    '<td><select type="text" class="form-control">'+ sup_acc_ass_dropdwn +'</select></td>'+
    '<td><select type="text" class="form-control">'+ sup_acc_ass_val_dropdwn +'</select></td>'+
    '<td><select type="text" class="form-control">'+ currency_dropdwn +'</select></td>'+
    '<td class="class_del_checkbox" hidden> <input type="checkbox" required> </td>'+
    '<td hidden><input type="text" id="workflow_acc_guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}


// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.account_assign_cat = row.find("TD").eq(2).html();
        main_attribute.acc_value = row.find("TD").eq(3).html();
        main_attribute.app_username = row.find("TD").eq(4).html();
        main_attribute.sup_company_id = row.find("TD").eq(5).html();
        main_attribute.sup_account_assign_cat = row.find("TD").eq(6).html();
        main_attribute.sup_acc_value = row.find("TD").eq(7).html();
        main_attribute.sup_currency_id = row.find("TD").eq(8).html();
        var wfacc_compare_maintable = main_attribute.company_id+'-'+main_attribute.account_assign_cat+'-'+main_attribute.acc_value+'-'+main_attribute.app_username+'-'+main_attribute.sup_company_id+'-'+main_attribute.sup_account_assign_cat+'-'+main_attribute.sup_acc_value+'-'+main_attribute.sup_currency_id
        main_table_low_value.push(wfacc_compare_maintable);
    });
    table_sort_filter('display_basic_table');
}

//********************************
    function delete_duplicate() {
        $('#id_popup_table').DataTable().destroy();
        var wfacc_code_check = new Array
        var main_table_low_value = new Array
        wfacc_data = new Array();
        $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        wfacc = {};
        checked_box = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
        wfacc.company_id = row.find("TD").eq(1).find('select[type="text"]').val();
        wfacc.account_assign_cat = row.find("TD").eq(2).find('select[type="text"]').val();
        wfacc.acc_value = row.find("TD").eq(3).find('select[type="text"]').val();
        wfacc.app_username = row.find("TD").eq(4).find('select[type="text"]').val();
        wfacc.sup_company_id = row.find("TD").eq(5).find('select[type="text"]').val();
        wfacc.sup_account_assign_cat = row.find("TD").eq(6).find('select[type="text"]').val();
        wfacc.sup_acc_value = row.find("TD").eq(7).find('select[type="text"]').val();
        wfacc.sup_currency_id = row.find("TD").eq(8).find('select[type="text"]').val();
        wfacc.workflow_acc_guid = row.find("TD").eq(9).find('input[type="text"]').val();
        if (wfacc == undefined) {
            wfacc.app_username = row.find("TD").eq(4).find('select[type="text"]').val();
        }
        if(wfacc.workflow_acc_guid == undefined) {
            wfacc.workflow_acc_guid = ''
        }
        var wfacc_compare = wfacc.company_id +'-'+  wfacc.account_assign_cat +'-'+ wfacc.acc_value +'-'+ wfacc.app_username +'-'+ wfacc.sup_company_id +'-'+wfacc.sup_account_assign_cat +'-'+ wfacc.sup_acc_value +'-'+ wfacc.sup_currency_id
                if (checked_box){
                    del_ind = '1'
                }
                else{
                        del_ind = '0'
                        if (wfacc_code_check.includes(wfacc_compare)) {
                            $(row).remove();
                        }
                        wfacc_code_check.push(wfacc_compare);
                        wfacc_data.push(wfacc);
                          main_table_low_value = get_main_table_data_upload(); //Read data from main table
                        if (main_table_low_value.includes(wfacc_compare)) {
                            $(row).remove();
                        }
                        main_table_low_value.push(wfacc_compare);
                }

        })
        table_sort_filter_popup_pagination('id_popup_table')
        check_data()
    }




// Function to get main table data
function get_main_table_data_upload() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.account_assign_cat = row.find("TD").eq(2).html();
        main_attribute.acc_value = row.find("TD").eq(3).html();
        main_attribute.app_username = row.find("TD").eq(4).html();
        main_attribute.sup_company_id = row.find("TD").eq(5).html();
        main_attribute.sup_account_assign_cat = row.find("TD").eq(6).html();
        main_attribute.sup_acc_value = row.find("TD").eq(7).html();
        main_attribute.sup_currency_id = row.find("TD").eq(8).html();
        main_attribute.del_ind = row.find("TD").eq(9).find('input[type="checkbox"]').is(':checked');
        var wfacc_compare_maintable = main_attribute.company_id+'-'+main_attribute.account_assign_cat+'-'+main_attribute.acc_value+'-'+main_attribute.app_username+'-'+main_attribute.sup_company_id+'-'+main_attribute.sup_account_assign_cat+'-'+main_attribute.sup_acc_value+'-'+main_attribute.sup_currency_id
        main_table_low_value.push(wfacc_compare_maintable);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}
// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var workflowaccounting_arr_obj ={};
        workflowaccounting_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(workflowaccounting_arr_obj.del_ind){
            workflowaccounting_arr_obj.company_id = row.find("TD").eq(1).html();
            workflowaccounting_arr_obj.account_assign_cat = row.find("TD").eq(2).html();
            workflowaccounting_arr_obj.acc_value = row.find("TD").eq(3).html();
            workflowaccounting_arr_obj.app_username = row.find("TD").eq(4).html();
            workflowaccounting_arr_obj.sup_company_id = row.find("TD").eq(5).html();
            workflowaccounting_arr_obj.sup_account_assign_cat = row.find("TD").eq(6).html();
            workflowaccounting_arr_obj.sup_acc_value = row.find("TD").eq(7).html();
            workflowaccounting_arr_obj.sup_currency_id = row.find("TD").eq(8).html();
            workflowaccounting_arr_obj.workflow_acc_guid = row.find("TD").eq(9).html();
            main_table_workflowaccounting_checked.push(workflowaccounting_arr_obj);
        }
    });
}

//*********************************************************
function account_assignment_value_find(company_num) {
    corresponding_values = {};
    corresponding_values.acc_ass_dropdwn = '';
    corresponding_values.acc_ass_val_dropdwn = '';
    corresponding_values.other_dropdn = '';
    company_list = company_list;
    unique_acct_cat= [];
    unique_acct_assmt_val = [];
    for (var i = 0; i < company_list.length; i++) {
        compare_dict = {};
        compare_dict = company_list[i]
        if (company_num == compare_dict.company_id && compare_dict.account_assign_cat != 'GLACC') {
            unique_acct_cat.push(compare_dict.account_assign_cat);
            unique_acct_assmt_val.push(compare_dict.acc_ass_val_dropdwn);
        }
    }
    arrDistinct = [];
    $(unique_acct_cat).each(function (index, item) {
        if ($.inArray(item, arrDistinct) == -1)
            arrDistinct.push(item);
    });
    for (var i = 0; i < arrDistinct.length; i++) {
        corresponding_values.other_dropdn += '<option value="'+arrDistinct[i]+'">' + arrDistinct[i] + '</option>'
    }
    assmtCatDistinct = [];
    $(unique_acct_cat).each(function (index, item) {
        if (item != 'GLACC' && $.inArray(item, assmtCatDistinct) == -1)
            assmtCatDistinct.push(item);
    });
    for (var i = 0; i < assmtCatDistinct.length; i++) {
        corresponding_values.acc_ass_dropdwn += '<option value="'+assmtCatDistinct[i]+'">' + assmtCatDistinct[i] + '</option>'
    }
    assmtValDistinct = [];
    $(unique_acct_assmt_val).each(function (index, item) {
        if ($.inArray(item, assmtValDistinct) == -1)
            assmtValDistinct.push(item);
    });
    for (var i = 0; i < assmtValDistinct.length; i++) {
        corresponding_values.acc_ass_val_dropdwn += '<option value="'+assmtValDistinct[i]+'">' + assmtValDistinct[i] + '</option>'
    }
    return corresponding_values
}

//**************************************************
function account_assignment_cat(acct_cat, comp_num) {
    corresponding_values = {};
    corresponding_values.acc_ass_val_dropdwn = '';
    company_list = company_list;
    unique_acct_assmt_val = [];
    var assmtValDistinct = [];
     for (var i = 0; i < company_list.length; i++) {
        compare_dict = {};
        compare_dict = company_list[i]
        if ((acct_cat == compare_dict.account_assign_cat) && (comp_num == compare_dict.company_id)) {
            unique_acct_assmt_val.push(compare_dict.acc_ass_val_dropdwn);
        }
        assmtValDistinct = [];
        $(unique_acct_assmt_val).each(function (index, item) {
        if ($.inArray(item, assmtValDistinct) == -1)
            assmtValDistinct.push(item);
        });
    }
    for (var i = 0; i < assmtValDistinct.length; i++) {
            corresponding_values.acc_ass_val_dropdwn += '<option value="'+assmtValDistinct[i]+'">'+assmtValDistinct[i]+'</option>'
    }
    return corresponding_values
}

//*************************************
function company_dropdwn_change(row){
    row.find("TD").eq(2).find("select").empty()
    row.find("TD").eq(3).find("select").empty()
    company_num = row.find("TD").eq(1).find("select option:selected").val();
    var comp_val = account_assignment_value_find(company_num)
    row.find("TD").eq(2).find("select").append(comp_val.acc_ass_dropdwn)
    row.find("TD").eq(3).find("select").append(comp_val.acc_ass_val_dropdwn)
}

//*************************************
function supcompany_dropdwn_change(row) {
    row.find("TD").eq(6).find("select").empty()
    row.find("TD").eq(7).find("select").empty()
    company_num = row.find("TD").eq(5).find("select option:selected").val();
    var comp_val = account_assignment_value_find(company_num)
    row.find("TD").eq(6).find("select").append(comp_val.acc_ass_dropdwn)
    row.find("TD").eq(7).find("select").append(comp_val.acc_ass_val_dropdwn)
}

//*************************************
function acc_ass_cat_dropdwn(row,company_num){
    acct_cat = row.find("TD").eq(2).find("select option:selected").val();
    row.find("TD").eq(3).find("select").empty();
    var acct_cat_val = account_assignment_cat(acct_cat,company_num)
    row.find("TD").eq(3).find("select").append(acct_cat_val.acc_ass_val_dropdwn)
}

//*************************************
function sup_acc_ass_cat_dropdwn(row,company_num){
    sup_acct_cat = row.find("TD").eq(6).find("select option:selected").val();
    row.find("TD").eq(7).find("select").empty();
    var acct_cat_val = account_assignment_cat(sup_acct_cat,company_num)
    row.find("TD").eq(7).find("select").append(acct_cat_val.acc_ass_val_dropdwn)
}

  // onclick of valid popup
    function valid_popup(){
      $('#id_data_upload').modal('hide');
      $("#valid_upload").modal('show');
    }