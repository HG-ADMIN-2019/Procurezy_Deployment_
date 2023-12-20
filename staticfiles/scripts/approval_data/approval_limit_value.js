var alv_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var alv={};

  // onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "alv_upload"
    $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
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
    $('#applimit_value_Modal').modal('hide');;
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_alv_code").prop("hidden", true);
    $("#id_error_msg_alv_name").prop("hidden", true);
    $("#id_error_msg_alv_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_alv_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_alv_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.company_id + '</td><td>' + item.app_types + '</td><td>' + item.app_code_id + '</td><td>' + item.upper_limit_value + '</td><td>' + item.currency_id + '</td><td hidden>' + item.app_lim_dec_guid + '</td></tr>';
    });
    $('#id_alv_tbody').append(edit_basic_data);
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

//****************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var alv_code_check = new Array
     var main_table_low_value = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        app_code_id = row.find("TD").eq(3).find('input[type="text"]').val().toUpperCase();
        company_id = row.find("TD").eq(1).find("select option:selected").val();
        app_types = row.find("TD").eq(2).find("select option:selected").val();
        currency_id = row.find("TD").eq(5).find("select option:selected").val();
        upper_limit_value = row.find("TD").eq(4).find('input[type="number"]').val().toUpperCase();
        app_lim_dec_guid = row.find("TD").eq(6).find('input[type="text"]').val().toUpperCase()
        alv_compare = alv.app_code_id +'-'+ alv.app_types +'-'+ alv.company_id
        if (alv_code_check.includes(alv_compare)) {
            $(row).remove();
        }
        alv_code_check.push(alv_compare);
          main_table_low_value = get_main_table_data_upload(); //Read data from main table
        if (main_table_low_value.includes(alv_compare)) {
            $(row).remove();
        }
        main_table_low_value.push(alv_compare);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#applimit_value_Modal').modal('hide');
    alv_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    validate_add_attributes = [];
    var alv_data = new Array();
    var alv={};
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        alv = {};
        alv.del_ind = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
        alv.app_code_id = row.find("TD").eq(3).find('input[type="text"]').val().toUpperCase();
        alv.company_id = row.find("TD").eq(1).find("select option:selected").val();
        alv.app_types = row.find("TD").eq(2).find("select option:selected").val();
        alv.currency_id = row.find("TD").eq(5).find("select option:selected").val();
        alv.upper_limit_value = row.find("TD").eq(4).find('input[type="number"]').val();
        alv.app_lim_dec_guid = row.find("TD").eq(6).find('input[type="text"]').val().toUpperCase()
        if (alv == undefined) {
            alv.app_code_id = row.find("TD").eq(3).find('input[type="text"]').val();
        }
        if(alv.app_lim_dec_guid  == undefined) {
            alv.app_lim_dec_guid  = ''
        }
        var alv_compare = alv.app_code_id +'-'+ alv.company_id +'-'+ alv.app_types+'-'+alv.currency_id
        validate_add_attributes.push(alv_compare);
        alv_data.push(alv);
    });
    table_sort_filter('id_popup_table');
    return alv_data;
}

function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#applimit_value_Modal').modal('show');
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">'+company_id_dropdown+'</select></td><td><select class="form-control">'+ approval_type_dropdown +'</select></td><td><input class="form-control check_special_char" type="text" maxlength="8"  name="approver_code" style="text-transform:uppercase;" required></td><td><input class="form-control" type="number" name="upper_limit_value" required></td><td><select class="form-control">'+currency_id_dropdown+'</select></td><td hidden><input type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var alv_arr_obj = {};
        alv_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(alv_arr_obj.del_ind){
            alv_arr_obj.app_code_id = row.find("TD").eq(3).html();
            alv_arr_obj.company_id = row.find("TD").eq(1).html();
            alv_arr_obj.app_types = row.find("TD").eq(2).html();
            alv_arr_obj.currency_id = row.find("TD").eq(5).html();
            alv_arr_obj.upper_limit_value = row.find("TD").eq(4).html();
            alv_arr_obj.app_lim_dec_guid = row.find("TD").eq(6).html();
            main_table_alv_checked.push(alv_arr_obj);
        }
    });
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.app_code_id = row.find("TD").eq(3).html();
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.app_types = row.find("TD").eq(2).html();
        main_attribute.currency_id = row.find("TD").eq(5).html();
        var alv_compare_maintable = main_attribute.app_code_id +'-'+ main_attribute.company_id +'-'+main_attribute.app_types +'-'+ main_attribute.currency_id
        main_table_low_value.push(alv_compare_maintable);
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
        main_attribute.app_code_id = row.find("TD").eq(3).html();
        main_attribute.company_id = row.find("TD").eq(1).html();
        main_attribute.app_types = row.find("TD").eq(2).html();
        main_attribute.currency_id = row.find("TD").eq(5).html();
        main_attribute.del_ind = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
        var alv_compare_maintable = main_attribute.app_code_id +'-'+ main_attribute.company_id +'-'+main_attribute.app_types +'-'+ main_attribute.currency_id + '-'+ main_attribute.del_ind
        main_table_low_value.push(alv_compare_maintable);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}