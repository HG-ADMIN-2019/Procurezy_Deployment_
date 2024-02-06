$(document).ready(function () {
    $('.block_date').datepicker({
        format: "yyyy-mm-dd",

    });
});

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}


//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');;
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>' +
        '<td><input class="input"  type="text"  onkeypress="return /[a-z]/i.test(event.key)" name="supplier_id" style="text-transform:uppercase;" required></td>' +
        '<td><input class="input" type="text" maxlength="40" onkeypress="return /[a-z ]/i.test(event.key)" name="supp_type"  pattern="[A-Z]" style="text-transform:uppercase;" required></td>' +
        '<td><input class="input" type="text" maxlength="40" onkeypress="return /[a-z ]/i.test(event.key)" name="name1"  pattern="[A-Z]" style="text-transform:uppercase;" required></td>' +
        '<td><input class="input" type="text" maxlength="40" onkeypress="return /[a-z ]/i.test(event.key)" name="name2"  pattern="[A-Z]" style="text-transform:uppercase;"></td>' +
        '<td><input class="input" type="text" maxlength="40" onkeypress="return /[a-z ]/i.test(event.key)" name="city"  pattern="[A-Z]" style="text-transform:uppercase;"></td>' +
        '<td><input class="input" type="text" maxlength="10"  name="postal_code" ></td>' +
        '<td><input class="input" type="text" maxlength="10" onkeypress="return /[a-z ]/i.test(event.key)" name="street"  pattern="[A-Z]" ></td>' +
        '<td><input class="input" type="text" maxlength="30" onkeypress="return /[a-z ]/i.test(event.key)" name="landline"  pattern="[A-Z]"></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="mobile_num" ></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="fax"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email" required></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email1"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email2"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email3"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email4"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email5"></td>' +
        '<td><input class="input" type="text" maxlength="10"  name="output_medium"></td>' +
        '<td><input class="input" type="text" maxlength="20"  name="search_term1"></td>' +
        '<td><input class="input" type="text" maxlength="20"  name="search_term2"></td>' +
        '<td><input class="input" type="text" maxlength="10"  name="duns_number"></td>' +
        '<td><input class="input" type="date"   name="block_date"></td>' +
        '<td><input class="input" type="text"  name="block"></td>' +
        '<td><input class="input" type="text" maxlength="13"  name="working_days"></td>' +
        '<td><input class="input" type="text" maxlength="10"  name="is_active"></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="registration_number"></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="country_code"></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="currency_id"></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="language_id"></td>' +
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>' +
        '<td hidden><input  type="text"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "supplier_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_supplier_id").prop("hidden", true);
    $("#id_error_msg_supp_email").prop("hidden", true);
    $("#id_error_msg_supplier_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//validate by comparing  main table values and popup table values
function maintable_validation(validate_add_attributes, main_table_low_value) {

    var no_duplicate_entries = 'Y'
    var common = [];
    jQuery.grep(validate_add_attributes, function (el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) { common.push(el); }
    });
    if (common.length != 0) {
        $("#id_error_msg").prop("hidden", false)
      
         var msg = "JMSG001";
         var msg_type ;
         msg_type = message_config_details(msg);
         $("#error_msg_id").prop("hidden", false)
         var display1 = msg_type.messages_id_desc;
        document.getElementById("id_error_msg").innerHTML = display1 + "for Supplier Id";
        document.getElementById("id_error_msg").style.color = "Red";
        // document.getElementById("supplier_id").style.border = "1px solid #FF0000";

        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');;
        no_duplicate_entries = 'N'
    }
    return no_duplicate_entries
}


function maintable_validation_email(validate_email_attributes, main_table_email_value) {

    var no_duplicate_email = 'Y'
    var common = [];
    jQuery.grep(validate_email_attributes, function (el) {

        if (jQuery.inArray(el, main_table_email_value) != -1) { common.push(el); }
    });
    if (common.length != 0) {
        $("#id_error_msg").prop("hidden", false)
                 
                    var msg = "JMSG024";
                    var msg_type ;
                  msg_type = message_config_details(msg);
                  $("#error_msg_id").prop("hidden", false)

                  if(msg_type.message_type == "ERROR"){
                        display_message("error_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "WARNING"){
                     display_message("id_warning_msg_id", msg_type.messages_id_desc)
                  }
                  else if(msg_type.message_type == "INFORMATION"){
                     display_message("id_info_msg_id", msg_type.messages_id_desc)
                  }
                  var display2 =  msg_type.messages_id_desc;
                  document.getElementById("id_error_msg").innerHTML = display2;

        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');;
        no_duplicate_email = 'N'
    }
    return no_duplicate_email,display2
}

function maintable_validation_reg_num(validate_email_attributes, main_table_reg_num) {

    var no_duplicate_regnum = 'Y'
    var common = [];
    jQuery.grep(validate_email_attributes, function (el) {
        if (jQuery.inArray(el, main_table_reg_num) != -1) { common.push(el); }
    });
    if (common.length != 0) {
        $("#id_error_msg").prop("hidden", false)
        document.getElementById("id_error_msg").innerHTML = messageConstants["JMSG001"] + "for Registration Number";
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');;
        no_duplicate_regnum = 'N'
    }
    return no_duplicate_regnum
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>' +
        '<td><input class="input"  type="text"  name="supplier_id"  required></td>' +
        '<td><input class="input" type="text"  name="supp_type"  ></td>' +
        '<td><input class="input" type="text" maxlength="40" onkeypress="return /[a-z ]/i.test(event.key)" name="name1"  pattern="[A-Z]"  required></td>' +
        '<td><input class="input" type="text" maxlength="40" onkeypress="return /[a-z ]/i.test(event.key)" name="name2"  pattern="[A-Z]" ></td>' +
        '<td><input class="input" type="text" maxlength="40" onkeypress="return /[a-z ]/i.test(event.key)" name="city"  pattern="[A-Z]" ></td>' +
        '<td><input class="input" type="text" maxlength="10"  name="postal_code"></td>' +
        '<td><input class="input" type="text" maxlength="10" onkeypress="return /[a-z ]/i.test(event.key)" name="street"  pattern="[A-Z]" ></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="landline" ></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="mobile_num" ></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="fax"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email" required></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email1"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email2"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email3"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email4"></td>' +
        '<td><input class="input" type="text" maxlength="100"  name="email5"></td>' +
        '<td><input class="input" type="text" maxlength="10"  name="output_medium"></td>' +
        '<td><input class="input" type="text" maxlength="20"  name="search_term1"></td>' +
        '<td><input class="input" type="text" maxlength="20"  name="search_term2"></td>' +
        '<td><input class="input" type="text" maxlength="10"  name="duns_number"></td>' +
        '<td><input class="input" type="date"   name="block_date"></td>' +
        '<td><input class="input" type="text"  name="block"></td>' +
        '<td><input class="input" type="text" maxlength="13"  name="working_days"></td>' +
        '<td><input class="input" type="text" maxlength="10"  name="is_active"></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="registration_number"></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="country_code" style="text-transform:uppercase;"></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="currency_id" style="text-transform:uppercase;"></td>' +
        '<td><input class="input" type="text" maxlength="30"  name="language_id" style="text-transform:uppercase;"></td>' +
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>' +
        '<td hidden><input  type="text"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "supplier_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_supplier_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_supp_data, function (i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>' +
            '<td>' + item.supplier_id + '</td>' +
            '<td>' + item.supp_type + '</td>' +
            '<td>' + item.name1 + '</td>' +
            '<td>' + item.name2 + '</td>' +
            '<td>' + item.city + '</td>' +
            '<td>' + item.postal_code + '</td>' +
            '<td>' + item.street + '</td>' +
            '<td>' + item.landline + '</td>' +
            '<td>' + item.mobile_num + '</td>' +
            '<td hidden>' + item.fax + '</td>' +
            '<td>' + item.email + '</td>' +
            '<td hidden>' + item.email1 + '</td>' +
            '<td hidden>' + item.email2 + '</td>' +
            '<td hidden>' + item.email3 + '</td>' +
            '<td hidden>' + item.email4 + '</td>' +
            '<td hidden>' + item.email5 + '</td>' +
            '<td hidden>' + item.output_medium + '</td>' +
            '<td hidden>' + item.search_term1 + '</td>' +
            '<td hidden>' + item.search_term2 + '</td>' +
            '<td hidden>' + item.duns_number + '</td>' +
            '<td hidden>' + item.block_date + '</td>' +
            '<td hidden>' + item.block + '</td>' +
            '<td hidden>' + item.working_days + '</td>' +
            '<td hidden>' + item.is_active + '</td>' +
            '<td hidden>' + item.registration_number + '</td>' +
            '<td hidden>' + item.country_code + '</td>' +
            '<td hidden>' + item.currency_id + '</td>' +
            '<td hidden>' + item.language_id + '</td>' +

            '<td hidden>' + item.supp_guid + '</td></tr>';
    });
    $('#id_supplier_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');

    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');

    table_sort_filter('display_basic_table');
}


//var main_table_country_checked = [];
//check function restricting special char and diaplay the data count of csv file
function check_data() {
    $('#id_popup_table').DataTable().destroy();
    $("#id_check_success_messages").empty()
    $("#id_check_error_messages").empty()
    $("#id_check_success_messages").prop("hidden", true)
    $("#id_check_error_messages").prop("hidden", true)
    $("#id_check_special_character_messages").prop("hidden", true)
    document.getElementById("id_error_msg_supplier_id").innerHTML = "";
    document.getElementById("id_error_msg_supp_email").innerHTML = "";
    document.getElementById("id_error_msg_supplier_length").innerHTML = "";
    count = 0;
    var supplier_array = new Array
    var DB_array = new Array
    var supplier_list = new Array
    var supplier_id_check = new Array
    del_ind = ''
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        supplier_id = row.find("TD").eq(1).find('input[type="text"]').val();
        supp_type = row.find("TD").eq(2).find('input[type="text"]').val();
        name1 = row.find("TD").eq(3).find('input[type="text"]').val();
        name2 = row.find("TD").eq(4).find('input[type="text"]').val();
        city = row.find("TD").eq(5).find('input[type="text"]').val();
        postal_code = row.find("TD").eq(6).find('input[type="text"]').val();
        street = row.find("TD").eq(7).find('input[type="text"]').val();
        landline = row.find("TD").eq(8).find('input[type="text"]').val();
        mobile_num = row.find("TD").eq(9).find('input[type="text"]').val();
        fax = row.find("TD").eq(10).find('input[type="text"]').val();
        email = row.find("TD").eq(11).find('input[type="text"]').val();
        email1 = row.find("TD").eq(12).find('input[type="text"]').val();
        email2 = row.find("TD").eq(13).find('input[type="text"]').val();
        email3 = row.find("TD").eq(14).find('input[type="text"]').val();
        email4 = row.find("TD").eq(15).find('input[type="text"]').val();
        email5 = row.find("TD").eq(16).find('input[type="text"]').val();
        output_medium = row.find("TD").eq(17).find('input[type="text"]').val();
        search_term1 = row.find("TD").eq(18).find('input[type="text"]').val();
        search_term2 = row.find("TD").eq(19).find('input[type="text"]').val();
        duns_number = row.find("TD").eq(20).find('input[type="text"]').val();
        block_date = row.find("TD").eq(21).find('input[type="date"]').val();
        block = row.find("TD").eq(22).find('input[type="text"]').val();
        working_days = row.find("TD").eq(23).find('input[type="text"]').val();
        is_active = row.find("TD").eq(24).find('input[type="text"]').val();
        registration_number = row.find("TD").eq(25).find('input[type="text"]').val();
        country_code = row.find("TD").eq(26).find('input[type="text"]').val().toUpperCase();
        currency_id = row.find("TD").eq(27).find('input[type="text"]').val().toUpperCase();
        language_id = row.find("TD").eq(28).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(30).find('input[type="checkbox"]').is(':checked')

        if (checked_box) {
            del_ind = '1'
        }
        else {
            del_ind = '0'
        }

        supplier_list.push([supplier_id, supp_type, name1, name2, city, postal_code, street, landline, mobile_num, fax, email, email1, email2, email3, email4, email5, output_medium, search_term1, search_term2, duns_number, block_date, block, working_days, is_active, registration_number, del_ind, country_code, currency_id, language_id])

        var format = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;


        //*************** checking for max length for country code (max length = 15) ***************
        if (supplier_id.length > 15) {
           
            var msg = "JMSG004";
            var msg_type ;
              msg_type = message_config_details(msg);
              $("#error_msg_id").prop("hidden", false)

              if(msg_type.message_type == "ERROR"){
                    display_message("error_msg_id", msg_type.messages_id_desc)
              }
              else if(msg_type.message_type == "WARNING"){
                 display_message("id_warning_msg_id", msg_type.messages_id_desc)
              }
              else if(msg_type.message_type == "INFORMATION"){
                 display_message("id_info_msg_id", msg_type.messages_id_desc)
              }
            var display8 = msg_type.messages_id_desc;
            document.getElementById("id_error_msg_supplier_length").innerHTML = display8+ "Country Code";
            $(row.find("TD").eq(1).find('input[type="text"]')).css("border", "1px solid #FF0000");
            count = count + 1;
        }

        if (supplier_id_check.includes(supplier_id)) {
            $(row).css("border", "#f8d7da");

        }
        else {
            $(row).css("border", "");
        }

        supplier_id_check.push(supplier_id)
    });

    //*************** shows save button if there are no errors(special characters and max length) ***************
    if (count == 0) {
        $("#id_check_special_character_messages").prop("hidden", true)
        $("#save_id").prop("hidden", false);
    }

}


function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var supplier_id_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        supplier_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        supp_type = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')
        supp_guid = row.find("TD").eq(4).find('input[type="text"]').val();

        if (supplier_id_check.includes(supplier_id)) {
            $(row).remove();
        }

        supplier_id_check.push(supplier_id);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}
