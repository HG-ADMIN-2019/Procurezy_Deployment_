var aav_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var used_acc_ass_cat = [];
var aav={};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#aav_Modal').modal('hide');
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "aav_upload"
    $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

//// on click Delete icon
//function onclick_delete_button() {
//    GLOBAL_ACTION = "DELETE"
//    onclick_copy_update_button("DELETE");
//    document.getElementById("id_del_add_button").style.display = "none";
//}

// on click copy icon display the selected checkbox data
function onclick_button_action(action) {
    GLOBAL_ACTION = action
    onclick_copy_update_button(action);
    if(action == 'UPDATE'){
        document.getElementById("id_del_add_button").style.display = "none";
        $("#save_id").prop("hidden", false);
    }
    else{
        document.getElementById("id_del_add_button").style.display = "block";
         $("#save_id").prop("hidden", false);
    }
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_aav_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_account_assignment_value, function(index, value) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + value.company_id + '</td><td>' + value.account_assign_cat + '</td><td>' + value.account_assign_value + '</td><td>' + format(value.valid_from) + '</td><td>' + format(value.valid_to)+ '</td><td hidden>' + value.account_assign_guid + '</td> <td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    });
    $('#id_aav_tbody').append(edit_basic_data);
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

//*******************************************
//function check_date_error(check_dates) {
//    date_error = "N"
//    $.each(check_dates, function(index, value){
//        var d1=new Date(value[0]); //yyyy-mm-dd
//        var d2=new Date(value[1]); //yyyy-mm-dd
//        if (d2< d1) {
//            get_message_details("JMSG017"); // Get message details
//            var display = msg_type.messages_id_desc;
//            document.getElementById("id_error_msg").innerHTML = display;
//            document.getElementById("id_error_msg").style.color = "Red";
//            $('#id_save_confirm_popup').modal('hide');
//            $('#aav_Modal').modal('show');
//            date_error = 'Y'
//        }
//    })
//    return date_error
//}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#aav_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_aav_code").prop("hidden", true);
    $("#id_error_msg_aav_name").prop("hidden", true);
    $("#id_error_msg_aav_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//**********************************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var aav_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************

        account_assign_value = row.find("TD").eq(3).find('input[type="number"]').val();
        valid_from = row.find("TD").eq(4).find('input[type="text"]').val()
        valid_to = row.find("TD").eq(5).find('input[type="text"]').val()
        account_assign_cat = row.find("TD").eq(2).find('Select').val()
        company_id = row.find("TD").eq(1).find('Select').val()
         var compare = account_assign_value + '-' + account_assign_cat + '-' + company_id+ '-' + valid_from+ '-' + valid_to
         if (aav_code_check.includes(compare)) {
            $(row).remove();
        }
        aav_code_check.push(compare);
        main_table_low_value = get_main_table_data_upload(); //Read data from main table
        if (main_table_low_value.includes(compare)) {
            $(row).remove();
        }
        main_table_low_value.push(compare);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    $("#save_id").prop("hidden", true);
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#aav_Modal').modal('hide');
    aav_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    validate_add_attributes = [];
    aav_data = new Array();
    var check_dates = []
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        aav={};
        aav.del_ind = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
        aav.company_id = row.find("TD").eq(1).find("select option:selected").val();
        aav.account_assign_cat = row.find("TD").eq(2).find('select option:selected').val()
        aav.account_assign_value = row.find("TD").eq(3).find('input[type="number"]').val();
        aav.valid_from = row.find("TD").eq(4).find('input[type="text"]').val()
        aav.valid_to = row.find("TD").eq(5).find('input[type="text"]').val()
        if((aav.valid_from == undefined) || (aav.valid_from == '')){
            aav.valid_from = '';
        }
        else
        {
//            var from_date = new Date(aav.valid_from).toISOString().slice(0, 10);
//            aav.valid_from = from_date;
        }
        if((aav.valid_to == undefined) || (aav.valid_to == '')){
            aav.valid_to = '';
        }
        else{
//            var to_date = new Date(aav.valid_to).toISOString().slice(0, 10);
//            aav.valid_to = to_date;
        }
        var compare = aav.company_id + '-' + aav.account_assign_cat + '-' + aav.account_assign_value;
        if (aav == undefined) {
            aav.account_assign_value = row.find("TD").eq(3).find('input[type="number"]').val();
        }
        if(aav.account_assign_guid == undefined) {
            aav.account_assign_guid = ''
        }
        check_dates.push([aav.valid_from, aav.valid_to])
        validate_add_attributes.push(compare);
        aav_data.push(aav);
    });
    table_sort_filter('id_popup_table');
    return aav_data;
}


//***************************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    $('#error_message').css('color', 'red');
    $('#error_msg_id').css('display', 'block');
    $('#id_save_confirm_popup').modal('hide');
    $('#aav_Modal').modal('show');
}

//*****************************
function check_date(aav) {
    var validDate = 'Y';
    var error_message = '';
    $.each(aav, function (i, item) {
        var validFromParts = item.valid_from.split('-');
        var validToParts = item.valid_to.split('-');
        var validFrom = new Date(validFromParts[2], validFromParts[1] - 1, validFromParts[0]);
        var validTo = new Date(validToParts[2], validToParts[1] - 1, validToParts[0]);
        var formattedValidFrom = validFrom.toLocaleDateString('en-GB');
        var formattedValidTo = validTo.toLocaleDateString('en-GB');

        if (validFrom > validTo) {
            $("#id_error_msg").prop("hidden", false);
            var msg = "JMSG017";
            var msg_type = message_config_details(msg);
            $("#error_msg_id").prop("hidden", false);

            if (msg_type.message_type == "ERROR") {
                display_message("error_msg_id", msg_type.messages_id_desc);
            } else if (msg_type.message_type == "WARNING") {
                display_message("id_warning_msg_id", msg_type.messages_id_desc);
            } else if (msg_type.message_type == "INFORMATION") {
                display_message("id_info_msg_id", msg_type.messages_id_desc);
            }

            var display = msg_type.messages_id_desc;
            $('#id_save_confirm_popup').modal('hide');
//            onclick_copy_update_button(item.account_assign_value);
            $('#aav_Modal').modal('show');
            validDate = 'N';
        }
    });
    return [validDate, error_message];
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
        main_attribute.account_assign_value = row.find("TD").eq(3).html();
        main_attribute.valid_from = row.find("TD").eq(4).find('input[type="text"]').val()
        main_attribute.valid_to = row.find("TD").eq(5).find('input[type="text"]').val()
        compare_maintable = main_attribute.company_id + '-' + main_attribute.account_assign_cat + '-' + main_attribute.account_assign_value +
        '-' + main_attribute.valid_from +'-' + main_attribute.valid_to +'-'+ main_attribute.del_ind;
        main_table_low_value.push(compare_maintable);
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
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.account_assign_cat = row.find("TD").eq(2).html();
        main_attribute.account_assign_value = row.find("TD").eq(3).html();
        main_attribute.valid_from = row.find("TD").eq(4).find('input[type="text"]').val()
        main_attribute.valid_to = row.find("TD").eq(5).find('input[type="text"]').val()
        main_attribute.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        compare_maintable = main_attribute.company_id + '-' + main_attribute.account_assign_cat + '-' + main_attribute.account_assign_value +
        '-' + main_attribute.valid_from + '-' + main_attribute.valid_to + '-'+ main_attribute.del_ind;
        main_table_low_value.push(compare_maintable);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        var aav_arr_obj = {};
         aav_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
         disable_check = row.find("TD").eq(7).find('input[type="text"]').val();
         if(aav_arr_obj.del_ind){
            aav_arr_obj.account_assign_value = row.find("TD").eq(3).find('input[type="number"]').val();
            aav_arr_obj.valid_from = row.find("TD").eq(4).find('input[type="text"]').val()
            aav_arr_obj.valid_to = row.find("TD").eq(5).find('input[type="text"]').val()
            aav_arr_obj.account_assign_cat = row.find("TD").eq(2).find('select option:selected').val()
            aav_arr_obj.company_id = row.find("TD").eq(1).find('select option:selected').val()
            aav_arr_obj.account_assign_guid = row.find("TD").eq(6).find('input').val()
            main_table_aav_checked.push(aav_arr_obj);
         }
    });
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_checked = [];
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var aav_arr_obj = {};
        aav_arr_obj.del_ind = checkbox.is(':checked');
        if(aav_arr_obj.del_ind) {
            aav_arr_obj.company_id = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html()
            aav_arr_obj.account_assign_cat = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            aav_arr_obj.account_assign_value = row.find("TD").eq(3).find('input[type="number"]').val() || row.find("TD").eq(3).html();
            aav_arr_obj.valid_from = row.find("TD").eq(4).find('input[type="text"]').val() || row.find("TD").eq(4).html();
            aav_arr_obj.valid_to = row.find("TD").eq(5).find('input[type="text"]').val() || row.find("TD").eq(5).html();
            aav_arr_obj.account_assign_guid = row.find("TD").eq(6).find('input').val() || row.find("TD").eq(6).html();
            main_table_checked.push(aav_arr_obj);
        }
    });
}

// storing company_code associated data from main table
function display_tb_data() {
    main_table_data = {};
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.account_assign_cat = row.find("TD").eq(2).html();
        if (!main_table_data.hasOwnProperty(main_attribute.company_id)) {
            main_table_data[main_attribute.company_id] = [];
        }
        main_table_data[main_attribute.company_id].push({
            account_assign_cat: main_attribute.account_assign_cat
        });
    });
    table_sort_filter('display_basic_table');
}

 // Function for add a new row data
 function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select class="form-control" id="company_dropdw" onchange="GetUnusedAccAssCat(this)">' + company_dropdwn + '</select></td>'+
    '<td><select class="form-control" id="acc_ass_val_dropdw">' + acc_ass_dropdwn + ' </select></td>'+
    '<td><input class="form-control check_number" type="number" minlength="4" maxlength="40" name="Account Assignment Value" required></td>'+
    '<td><input class="form-control formatDate" type="text"  name="valid_from" required></td>'+
    '<td><input class="form-control formatDate" type="text"  name="Valid To Date" required></td>'+
    '<td hidden><input value=""></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>'+
    '</tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    DatePicker();
    table_sort_filter("id_popup_table");
 }

// onchange function(filtering acc_ass_cat)
 function GetUnusedAccAssCat(company_code){
    var company_val = company_code.value;
    var company = $(company_code).closest('tr').find('.form-control').eq(0);
    var acc_ass_dropdwn = $(company_code).closest('tr').find('.form-control').eq(1);

    var acc_ass_cat = main_table_data[company_val];
    if(!acc_ass_cat){
        acc_ass_dropdwn.empty();
        $.each(rendered_aac_data, function(i, item) {
            acc_ass_dropdwn.append('<option value ="' + item.account_assign_cat + '" >' + item.account_assign_cat + '</option>')
        });
    } else {
        acc_ass_dropdwn.empty();
        var options = [];
        rendered_aac_data.forEach(item => {
            var found = acc_ass_cat.some(lang => lang.account_assign_cat === item.account_assign_cat);
            if (found) {
                used_acc_ass_cat.push(item.account_assign_cat)
            } else {
                options.push('<option value="' + item.account_assign_cat + '">' + item.account_assign_cat + '</option>');
            }
        })
        acc_ass_dropdwn.append(options.join(''));
    }
}

 // onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}