var detgl_data = new Array();
var main_table_low_value = [];
var validate_add_attributes = [];
var detgl={};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#Detgl_Modal').modal('hide');
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "detgl_upload"
    $("#id_error_msg_upload").prop("hidden",true)
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

//**************************************
function update_check_message(messages) {
     $.each(messages, function (i, message) {
        $("#id_check_success_messages").append('<p>' + message + '</p>')
     });
    $("#id_check_success_messages").prop("hidden",false)
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    display_button();
    onclick_copy_update_button('copy')
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of checkbox enable delete button in popup -> Dependency delete
function enableDeleteButton() {
    var $popupCheckboxes = $('#id_popup_table td .checkbox_check');
    var $deleteButton = $('#delete_data');
    // Check if any checkbox is checked in the popup
    var anyCheckboxChecked = $popupCheckboxes.is(":checked");
    // Enable or disable the delete button based on whether any checkbox is checked
    $deleteButton.prop('disabled', !anyCheckboxChecked || $popupCheckboxes.length === 0);
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none");
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });

    if (GLOBAL_ACTION == "detgl_upload") {
        basic_add_new_html = '<tr><td><input type="checkbox" required></td>' +
            '<td><select class="form-control">' + prod_cat_dropdown + '</select></td>' +
            '<td><select class="form-control">' + company_dropdown + '</select></td>' +
            '<td><select class="form-control">' + accasscat_dropdown + '</select></td>' +
            '<td><select class="form-control">' + glacc_dropdown + '</select></td>' +
            '<td><input type="checkbox" name="gl_acc_default" required></td>' +
            '<td><input class="form-control" type="number" min="1" name="From_value" required></td>' +
            '<td><input class="form-control" type="number" min="1" name="To_value" required></td>' +
            '<td><select class="form-control">' + currency_dropdown + '</select></td>' +
            '<td hidden><input type="text" class="form-control" value="GUID"></td>' +
            '<td class="class_del_checkbox"><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
        table_sort_filter('id_popup_table');
        $(".class_del_checkbox").prop("hidden", false);
        $("#id_del_ind_checkbox").prop("hidden", false);
        var company_num = '';
        $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            row.find("TD").eq(3).find("select").empty();
            row.find("TD").eq(4).find("select").empty();
            company_num = row.find("TD").eq(2).find("select option:selected").val();
            var assign_val = account_assignment_value_find(company_num);
            row.find("TD").eq(3).find("select").append(assign_val.acc_ass_dropdwn);
            row.find("TD").eq(4).find("select").append(assign_val.acc_ass_val_dropdwn);
            $(row.find("TD").eq(2).find("select")).change(function () {
                company_dropdwn_change(row);
            });
        });
    }
    else {
        new_row_data();   // Add a new row in popup
        var company_num = '';
        $("#id_popup_table").on("change", "select[name='company_dropdown']", function () {
            var row = $(this).closest("tr");
            company_dropdwn_change(row);
        });
        $("#id_popup_table").on("draw.dt", function () {
            $("#id_popup_table TBODY TR").each(function () {
                var row = $(this);
                row.find("TD").eq(3).find("select").empty();
                row.find("TD").eq(4).find("select").empty();
                company_num = row.find("TD").eq(2).find("select option:selected").val();
                var assign_val = account_assignment_value_find(company_num);
                row.find("TD").eq(3).find("select").append(assign_val.acc_ass_dropdwn);
                row.find("TD").eq(4).find("select").append(assign_val.acc_ass_val_dropdwn);
            });
        });
        $('#delete_data').hide();
    }
}



//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $("#Detgl_Modal").modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_Prod_cat_id").prop("hidden", true);
    $("#id_error_Fromvalue_lesserthan_Tovalue").prop("hidden", true);
    $("#id_error_FromvalueTovalue_positive_num").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//**********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#Detgl_Modal').modal('show');
}

// onclick of valid popup
function valid_popup(){
  $('#id_data_upload').modal('hide');
  $("#valid_upload").modal('show');
}

//****************************
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var detgl_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        gl_acc_num = row.find("TD").eq(4).find("select option:selected").val();
        gl_acc_default = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        account_assign_cat = row.find("TD").eq(3).find("select option:selected").val();
        company_id = row.find("TD").eq(2).find("select option:selected").val();
        item_from_value = row.find("TD").eq(6).find('input[type="number"]').val();
        item_to_value = row.find("TD").eq(7).find('input[type="number"]').val();
        currency_id = row.find("TD").eq(8).find("select option:selected").val();
        checked_box = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        var compare = gl_acc_num + '-' + company_id + '-' + account_assign_cat
        if (detgl_code_check.includes(compare)) {
            $(row).remove();
        }
        detgl_code_check.push(compare);
        main_table_low_value = get_main_table_data_upload(); //Read data from main table
        if (main_table_low_value.includes(compare)) {
            $(row).remove();
        }
        main_table_low_value.push(compare);
    });

    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#Detgl_Modal').modal('hide');
    detgl_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    detgl_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        detgl = {};
        detgl.del_ind = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
        detgl.prod_cat_id = row.find("TD").eq(1).find('select option:selected').val();
        detgl.company_id = row.find("TD").eq(2).find("select option:selected").val();
        detgl.account_assign_cat = row.find("TD").eq(3).find("select option:selected").val();
        detgl.gl_acc_num = row.find("TD").eq(4).find("select option:selected").val();
        detgl.gl_acc_default = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        detgl.item_from_value = row.find("TD").eq(6).find('input[type="number"]').val();
        detgl.item_to_value = row.find("TD").eq(7).find('input[type="number"]').val();
        detgl.currency_id = row.find("TD").eq(8).find("select option:selected").val();
        detgl.det_gl_acc_guid = row.find("TD").eq(9).find('input[type="text"]').val();
        var compare = detgl.prod_cat_id + '-' + detgl.company_id + '-' + detgl.account_assign_cat +'-'+ detgl.gl_acc_num
        if (detgl == undefined) {
            detgl.prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        validate_add_attributes.push(compare);
        detgl_data.push(detgl);
    });
    table_sort_filter('id_popup_table');
    return detgl_data;
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
    '<td><select class="form-control">' + prod_cat_dropdown + '</select></td>'+
    '<td><select name="company_dropdown" class="form-control">' + company_dropdown + '</select></td>'+
    '<td><select class="form-control">' + accasscat_dropdown + '</select></td>'+
    '<td><select class="form-control">' + glacc_dropdown + '</select></td>'+
    '<td><input type="checkbox" name="gl_acc_default" required></td>'+
    '<td><input class="form-control" type="number"  min="1" name="From_value"  required></td>'+
    '<td><input class="form-control" type="number"  min="1" name="To_value"  required></td>'+
    '<td><select class="form-control">' + currency_dropdown + '</select></td><td hidden><input type="text" class="form-control"  value="GUID"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    var table = $('#id_popup_table').DataTable();
    table.row.add($(basic_add_new_html)).draw();
    table_sort_filter('id_popup_table');
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.prod_cat_id = row.find("TD").eq(1).html();
        main_attribute.company_id = row.find("TD").eq(2).html();
        main_attribute.account_assign_cat = row.find("TD").eq(3).html();
        main_attribute.gl_acc_num= row.find("TD").eq(4).html();
        main_attribute.item_from_value = row.find("TD").eq(6).html();
        main_attribute.item_to_value = row.find("TD").eq(7).html();
        main_attribute.currency_id = row.find("TD").eq(8).html();
        var detgl_compare = main_attribute.prod_cat_id + '-' + main_attribute.company_id + '-' + main_attribute.account_assign_cat +'-'+ main_attribute.gl_acc_num
        main_table_low_value.push(detgl_compare);
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
        main_attribute.prod_cat_id = row.find("TD").eq(1).html();
        main_attribute.company_id = row.find("TD").eq(2).html();
        main_attribute.account_assign_cat = row.find("TD").eq(3).html();
        main_attribute.gl_acc_num= row.find("TD").eq(4).html();
        main_attribute.item_from_value = row.find("TD").eq(6).html();
        main_attribute.item_to_value = row.find("TD").eq(7).html();
        main_attribute.currency_id = row.find("TD").eq(8).html();
        var detgl_compare = main_attribute.prod_cat_id + '-' + main_attribute.company_id + '-' + main_attribute.account_assign_cat +'-'+ main_attribute.gl_acc_num
        main_table_low_value.push(detgl_compare);
    });
    table_sort_filter('display_basic_table');
    return main_table_low_value
}

// Function to get the selected row data
//function get_selected_row_data() {
//    $("#display_basic_table TBODY TR").each(function () {
//        var row = $(this);
//        var detgl_arr_obj = {};
//        detgl_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
//        if( detgl_arr_obj.del_ind){
//            detgl_arr_obj.prod_cat_id = row.find("TD").eq(1).html();
//            detgl_arr_obj.company_id = row.find("TD").eq(2).html();
//            detgl_arr_obj.account_assign_cat = row.find("TD").eq(3).html();
//            detgl_arr_obj.gl_acc_num = row.find("TD").eq(4).html();
//            detgl_arr_obj.gl_acc_default = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
//            detgl_arr_obj.item_from_value = row.find("TD").eq(6).html();
//            detgl_arr_obj.item_to_value = row.find("TD").eq(7).html();
//            detgl_arr_obj.currency_id = row.find("TD").eq(8).html();
//            detgl_arr_obj.det_gl_acc_guid = row.find("TD").eq(9).html();
//            main_table_detgl_checked.push(detgl_arr_obj);
//        }
//    });
//}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_checked = [];
    $(tableSelector).DataTable().$('td .checkbox_check').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var detgl_arr_obj = {};
        detgl_arr_obj.del_ind = checkbox.is(':checked');
        if(detgl_arr_obj.del_ind) {
            detgl_arr_obj.prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            detgl_arr_obj.company_id = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            detgl_arr_obj.account_assign_cat = row.find("TD").eq(3).find('input[type="text"]').val() || row.find("TD").eq(3).html();
            detgl_arr_obj.gl_acc_num = row.find("TD").eq(4).find('input[type="number"]').val() || row.find("TD").eq(4).html();
            detgl_arr_obj.gl_acc_default = row.find("TD").eq(5).find('input[name="gl_acc_default"]').is(':checked');
            detgl_arr_obj.item_from_value = row.find("TD").eq(6).find('input[type="number"]').val() || row.find("TD").eq(6).html();
            detgl_arr_obj.item_to_value = row.find("TD").eq(7).find('input[type="number"]').val() || row.find("TD").eq(7).html();
            detgl_arr_obj.currency_id = row.find("TD").eq(8).find('input[type="text"]').val() || row.find("TD").eq(8).html();
            detgl_arr_obj.det_gl_acc_guid = row.find("TD").eq(9).find('input[type="text"]').val() || row.find("TD").eq(9).html();
            main_table_checked.push(detgl_arr_obj);
        }
    });
}

//*********************************************************
function account_assignment_value_find(company_num) {
    corresponding_values = {};
    corresponding_values.acc_ass_dropdwn = '';
    corresponding_values.acc_ass_val_dropdwn = '';
    corresponding_values.other_dropdn = '';
    unique_acct_cat= [];
    unique_acct_assmt_val = [];
    for (var i = 0; i < rendered_acc_value_list.length; i++) {
        var item = rendered_acc_value_list[i];
        if (item.company_id == company_num) {
            for (var j = 0; j < item.account_assign_cat_list.length; j++) {
                var cat = item.account_assign_cat_list[j];
                var val = item.account_assign_cat_value_list[j];
                if (cat !== undefined && cat !== '-- Select Account Assignment Category --') {
                    unique_acct_cat.push(cat);
                }
                if (val !== undefined) {
                    unique_acct_assmt_val.push(val);
                }
            }
        }
    }
    unique_acct_cat = unique_acct_cat.filter(function(item) {
        return item !== undefined;
    });
    unique_acct_assmt_val = unique_acct_assmt_val.filter(function(item) {
        return item !== undefined;
    });
    for (var i = 0; i < arrDistinct.length; i++) {
        corresponding_values.other_dropdn += '<option value="'+arrDistinct[i]+'">' + arrDistinct[i] + '</option>'
    }
    assmtCatDistinct = [];
    $(unique_acct_cat).each(function (index, item) {
        if ($.inArray(item, assmtCatDistinct) == -1)
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
    return corresponding_values;
}



//***********************************88
function company_dropdwn_change(row){
    row.find("TD").eq(3).find("select").empty()
    row.find("TD").eq(4).find("select").empty()
    company_num = row.find("TD").eq(2).find("select option:selected").val();
    var comp_val = account_assignment_value_find(company_num)
    row.find("TD").eq(3).find("select").append(comp_val.acc_ass_dropdwn)
    row.find("TD").eq(4).find("select").append(comp_val.acc_ass_val_dropdwn)
}