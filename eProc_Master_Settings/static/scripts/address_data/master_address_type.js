var addresstype_data = new Array();
var main_table_low_value = [];
var validate_add_attributes = [];
var duplicate_entry = [];
var addresstype={};

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "addresstype_upload"
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
    onclick_copy_update_button("COPY")
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("UPDATE")
    document.getElementById("id_del_add_button").style.display = "none";
    $("#save_id").prop("hidden", false);
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Adrs_Type_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_address_type").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();


});

//*********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#Adrs_Type_Modal').modal('show');
}



//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_address_type_tbody').empty();
    var edit_basic_data = '';

    $.each(rendered_address_type_data, function (i, item) {
        var validFromDate = item.valid_from.split('T')[0].split('-').reverse().join('-');
        var validToDate = item.valid_to.split('T')[0].split('-').reverse().join('-');

        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>' +
        '<td>'+ item.company_id +'</td>'+
        '<td>' + item.address_type + '</td>' +
        '<td>' + item.address_number + '</td>' +
        '<td>'+ validFromDate +'</td>'+
        '<td>'+ validToDate +'</td>'+
        '<td hidden> <input type="checkbox"></td>' +
        '<td hidden>' + item.address_guid + '</td></tr>';
    });

    $('#id_address_type_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').hide();
    $('#id_delete_confirm_popup').hide();
    $('#id_check_all').hide();
    table_sort_filter('display_basic_table');
}




// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#Adrs_Type_Modal').modal('hide');
    addresstype_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    validate_add_attributes = [];
    addresstype_data = new Array();
    var check_dates = []
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        addresstype = {};
        addresstype.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        addresstype.address_guid = row.find("TD").eq(7).find('input').val();
        addresstype.address_number = row.find("TD").eq(3).find('select option:selected').val();
        addresstype.address_type = row.find("TD").eq(2).find('select option:selected').val();
        addresstype.company_id = row.find("TD").eq(1).find('select option:selected').val();
        addresstype.valid_from = row.find("TD").eq(4).find('input[type="text"]').val();
        addresstype.valid_to = row.find("TD").eq(5).find('input[type="text"]').val();
//        addresstype.valid_to = row.find("TD").eq(5).find('input[type="date"]').val();
        var address_compare = addresstype.address_number + '-' + addresstype.address_type + '-' + addresstype.company_id;
        if (addresstype == undefined) {
            addresstype.address_number = row.find("TD").eq(3).find('input').val();
        }
        if (addresstype.address_guid == undefined) {
            addresstype.address_guid = '';
        }
        check_dates.push([addresstype.valid_from, addresstype.valid_to]);
        validate_add_attributes.push(address_compare);
        addresstype_data.push(addresstype);
    });
    table_sort_filter('id_popup_table');
    return addresstype_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>' +
        '<td><select class="form-control">'+company_dropdwn+'</select></td>' +
        '<td><select class="form-control">'+address_type_dropdown+'</select></td>' +
        '<td><select class="form-control">'+address_number_dropdwn+'</select></td>' +
        '<td><input  type="text" name = "valid_from" class="form-control formatDate"></td>' +
        '<td><input type="text" name = "valid_to"  class="form-control formatDate"></td>' +
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>' +
        '<td hidden><input  type="text" class="form-control"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    DatePicker();
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.address_number = row.find("TD").eq(3).html();
        main_attribute.address_type = row.find("TD").eq(2).html();
        main_attribute.company_id = row.find("TD").eq(1).html();
        var address_compare_maintable = main_attribute.address_number +'-'+ main_attribute.address_type+'-'+main_attribute.company_id
        main_table_low_value.push(address_compare_maintable);
    });
    table_sort_filter('display_basic_table');
}


// Function to get main table data
function get_main_table_data_upload() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.address_number = row.find("TD").eq(3).html();
        main_attribute.address_type = row.find("TD").eq(2).html();
        main_attribute.company_id = row.find("TD").eq(1).html();
        var address_compare_maintable = main_attribute.address_number +'-'+ main_attribute.address_type+'-'+main_attribute.company_id
        main_table_low_value.push(address_compare_maintable);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}
 // Function to get the selected row data
 function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var address_type_arr_obj = {};
        address_type_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(address_type_arr_obj.del_ind ){
            address_type_arr_obj.address_guid = row.find("TD").eq(7).html();
             address_type_arr_obj.valid_to = row.find("TD").eq(5).html();
              address_type_arr_obj.valid_from = row.find("TD").eq(4).html();
             address_type_arr_obj.company_id = row.find("TD").eq(1).html();
            address_type_arr_obj.address_type = row.find("TD").eq(2).html();
            address_type_arr_obj.address_number = row.find("TD").eq(3).html();
            main_table_address_type_checked.push(address_type_arr_obj);
        }
    });
 }


//**********************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var address_type_code_check = new Array
     var main_table_low_value = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        //*************** reading data from the pop-up ***************

        address_guid = row.find("TD").eq(7).find('input').val();
        address_number = row.find("TD").eq(3).find('select option:selected').val();
        address_type = row.find("TD").eq(2).find('select option:selected').val();
        company_id = row.find("TD").eq(1).find('select option:selected').val();
        valid_from = row.find("TD").eq(4).find('input[type="text"]').val();
        valid_to = row.find("TD").eq(5).find('input[type="text"]').val();
        checked_box = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked')
        address_compare = address_number +'-'+ address_type+'-'+ company_id
       // Only proceed if address_number && address_type && company_id are not empty
     if (checked_box) {
            // Keep rows with the checkbox checked
            del_ind = '1';
     } else {
            del_ind = '0';
      if (address_number && address_type && company_id && valid_from && valid_to) {
        if (address_type_code_check.includes(address_compare)) {
            $(row).remove();
        }
        address_type_code_check.push(address_compare);
        main_table_low_value = get_main_table_data_upload(); //Read data from main table
        if (main_table_low_value.includes(address_compare)) {
            $(row).remove();
        }
        main_table_low_value.push(address_compare);
      }
     }
    })
    table_sort_filter_popup('id_popup_table')
    check_data()
}



function check_date(addresstype_data) {
    var validDate = 'Y';
    var error_message = ''
    $.each(addresstype_data, function (i, item) {
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
            $('#Adrs_Type_Modal').modal('show');
            validDate = 'N';
        }
    });
    return [validDate, error_message];
}


//*******************************************
function check_date_error(check_dates) {
    date_error = "N"
    $.each(check_dates, function(index, value){
        var d1=new Date(value[0]); //yyyy-mm-dd
        var d2=new Date(value[1]); //yyyy-mm-dd
        if (d2< d1) {
            get_message_details("JMSG017"); // Get message details
            var display = msg_type.messages_id_desc;
            document.getElementById("id_error_msg").innerHTML = display;
            document.getElementById("id_error_msg").style.color = "Red";
            $('#id_save_confirm_popup').modal('hide');
            $('#myModal').modal('show');
            date_error = 'Y'
        }
    })
    return date_error
}