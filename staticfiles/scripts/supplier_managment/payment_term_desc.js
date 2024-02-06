var payment_term_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var payment_term={};

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
    $("#save_id").prop("hidden", false);
}

 // onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "payterm_desc_upload"
     $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#Paytrm_desc_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_payment_term_key").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//**********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    $('#error_message').css('color', 'red');
    $('#error_msg_id').css('display', 'block');
    $('#id_save_confirm_popup').modal('hide');
    $('#aav_Modal').modal('show');
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#Paytrm_desc_Modal').modal('hide');
    payment_term_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});


//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    payment_term_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        payment_term = {};
        payment_term.language_id = row.find("TD").eq(1).find('select[type="text"]').val();
        payment_term.payment_term_key = row.find("TD").eq(2).find('select[type="text"]').val();
        payment_term.description = row.find("TD").eq(3).find('input[type="text"]').val();
        payment_term.day_limit = row.find("TD").eq(4).find('input[type="number"]').val();
        payment_term.payment_term_guid = row.find("TD").eq(6).find('input[type="text"]').val();
        payment_term.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        if (payment_term == undefined) {
            payment_term.payment_term_key = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        if (payment_term.payment_term_guid == undefined) {
            payment_term.payment_term_guid = '';
        }
        var paytrm_desc_compare = payment_term.language_id +'-'+ payment_term.payment_term_key
        validate_add_attributes.push(paytrm_desc_compare);
        payment_term_data.push(payment_term);
    });
    table_sort_filter('id_popup_table');
    return payment_term_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html ='<tr><td><input type="checkbox" required></td>'+
        '<td><select id="language" name="language" class="form-control"  type="text">'+language_dropdown+'</select></td>'+
        '<td><select id="payterm_key" name="payterm_key" class="form-control"  type="text">'+payment_term_dropdown+'</select></td>'+
        '<td><input  type="text"  name="description" class="form-control check_special_char" maxlength="50"></td>'+
        '<td><input  type="number"  name="day_limit" class="form-control check_number" maxlength="10"></td>'+
        '<td class="class_del_checkbox" hidden><input type="checkbox"></td>'+
        '<td hidden><input  type="text"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.language_id = row.find("TD").eq(1).html();
        main_attribute.payment_term_key = row.find("TD").eq(2).html();
//        var desc = get_language(render_language_data,main_attribute.language_id)
        var paytrm_desc_maintable = main_attribute.language_id +'-'+ main_attribute.payment_term_key
        main_table_low_value.push(paytrm_desc_maintable);
    });
    table_sort_filter('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var payment_term_arr_obj = {};
        var lang_desc;
        var lang_code;
        lang_desc = row.find("TD").eq(1).html();
        for (i = 0; i < render_language_data.length; i++) {
            if (lang_desc == render_language_data[i].description)
                lang_code = render_language_data[i].language_id
        }
        payment_term_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(payment_term_arr_obj.del_ind) {
            payment_term_arr_obj.language_id = lang_code;
            payment_term_arr_obj.payment_term_key = row.find("TD").eq(2).html();
            payment_term_arr_obj.day_limit = row.find("TD").eq(4).html();
            payment_term_arr_obj.description = row.find("TD").eq(3).html();
            payment_term_arr_obj.payment_term_guid = row.find("TD").eq(6).html();
            main_table_payment_term_checked.push(payment_term_arr_obj);
        }
    });
}

// Function to get the selected row data
function get_main_table_data_upload() {
     main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
            main_attribute.language_id = row.find("TD").eq(1).html();
            main_attribute.payment_term_key = row.find("TD").eq(2).html();            
            main_attribute.payment_term_guid = row.find("TD").eq(6).html();
            main_attribute.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            var compare = main_attribute.language_id +'-'+ main_attribute.payment_term_key
            main_table_low_value.push(compare);

    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}

    //********************************
    function delete_duplicate() {
        $('#id_popup_table').DataTable().destroy();
        var paymentermdesc_code_check = new Array
        var main_table_low_value = new Array
        $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        payment_term_desc = {};
        payment_term_desc.language_id = row.find("TD").eq(1).find('select[type="text"]').val();
        payment_term_desc.payment_term_key = row.find("TD").eq(2).find('select[type="text"]').val();
        payment_term_desc.description = row.find("TD").eq(3).find('input[type="text"]').val();
        payment_term_desc.day_limit = row.find("TD").eq(4).find('input[type="number"]').val();
        payment_term_desc.payment_term_guid = row.find("TD").eq(6).find('input[type="text"]').val();
        checked_box = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked')
        var compare = payment_term_desc.language_id +'-'+ payment_term_desc.payment_term_key
        if (checked_box){
                del_ind = '1'
        }
        else{
            del_ind = '0'
            if (paymentermdesc_code_check.includes(compare)) {
                $(row).remove();
            }
            paymentermdesc_code_check.push(compare);
            main_table_low_value = get_main_table_data_upload(); //Read data from main table
            if (main_table_low_value.includes(compare)) {
                $(row).remove();
            }
            main_table_low_value.push(payment_term_desc);
        }
        })
        table_sort_filter_popup_pagination('id_popup_table')
        check_data()
    }

