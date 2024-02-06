var purhcase_control_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var purchase_contrl = {};
var hidden_prod_cat_IDs = [];

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_pc_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_pc_data, function (i, item) {
        var data = '';
        if (item.purchase_ctrl_flag == true) {
            data = 'Activate'
        } else {
            data = 'Deactivate'
        }

        var call_off_desc = '';
        for (var j = 0; j < rendered_call_off.length; j++) {
            if (rendered_call_off[j].value === item.call_off) {
                call_off_desc = rendered_call_off[j].desc;
                break;
            }
            else {
                call_off_desc = item.call_off
            }
        }

        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.company_code_id + '</td><td>' + call_off_desc + '</td><td>' + item.prod_cat_id + '</td><td>' + data + '</td><td hidden>' + item.purchase_control_guid + '</td><td hidden>' + item.del_ind_flag + '</td></tr>';
    });
    $('#id_pc_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $(" input:checkbox ").prop('checked', false);
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

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#purchase_ctrl_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_pc_code").prop("hidden", true);
    $("#id_error_msg_pc_name").prop("hidden", true);
    $("#id_error_msg_pc_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

function display_error_message(error_message) {
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#purchase_ctrl_Modal').modal('show');
}

// Function to delete duplicates
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var pur_contrl_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************
        call_off = row.find("TD").eq(2).find('input[type="text"]').val();
        purchase_ctrl_flag = row.find("TD").eq(3).find('input[type="checkbox"]').val();
        company_id = row.find("TD").eq(1).find('input[type="text"]').val();
        checked_box = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked')
        if (pur_contrl_check.includes(company_id)) {
            $(row).remove();
        }
        pur_contrl_check.push(company_id);
    })
    table_sort_filter('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#purchase_ctrl_Modal').modal('hide');
    purhcase_control_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    purhcase_control_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        purchase_contrl = {};
        purchase_contrl.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        purchase_contrl.company_code_id = row.find("TD").eq(1).find('select[type="text"]').val();
        purchase_contrl.call_off = row.find("TD").eq(2).find('select[type="text"]').val().split("-")[0];
        purchase_contrl.prod_cat_id = row.find("TD").eq(3).find('select option:selected').val();
        purchase_contrl.purchase_ctrl_flag = row.find("TD").eq(4).find('select[type="text"]').val();
        purchase_contrl.purchase_control_guid = row.find("TD").eq(5).find('input[type="text"]').val();
        var data = '';
        if (purchase_contrl.purchase_ctrl_flag == 'Activate'){
            data = true
        } else{
            data = false
        }
        purchase_contrl.purchase_ctrl_flag  = data;
        if (purchase_contrl == undefined) {
            purchase_contrl.company_code_id = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        var compare = purchase_contrl.company_code_id + '-' + purchase_contrl.call_off + '-' + purchase_contrl.prod_cat_id
        validate_add_attributes.push(compare);
        purhcase_control_data.push(purchase_contrl);
    });
    table_sort_filter('id_popup_table');
    return purhcase_control_data;
}

// Function to get main table data
function get_main_table_data() {
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.company_code_id = row.find("TD").eq(1).html();
        main_attribute.call_off = row.find("TD").eq(2).html();
        main_attribute.prod_cat_id = row.find("TD").eq(3).html();
        main_attribute.purchase_ctrl_flag = row.find("TD").eq(4).html();
        var data = '';
        if (main_attribute.purchase_ctrl_flag == 'Activate') {
            data = true
        } else {
            data = false
        }
        main_attribute.purchase_ctrl_flag = data;
        main_attribute.purchase_control_guid = row.find("TD").eq(5).html();
        var compare_maintable = main_attribute.company_code_id + '-' + main_attribute.call_off + '-' + main_attribute.prod_cat_id
        main_table_low_value.push(compare_maintable);
    });
    table_sort_filter_page('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data() {
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var purchase_contrl_type_dic = {};
        purchase_contrl_type_dic.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
         if (purchase_contrl_type_dic.del_ind) {
            purchase_contrl_type_dic.company_code_id = row.find("TD").eq(1).html();
            purchase_contrl_type_dic.call_off = row.find("TD").eq(2).html().split("-")[0];
            purchase_contrl_type_dic.prod_cat_id = row.find("TD").eq(3).html();
            purchase_contrl_type_dic.purchase_ctrl_flag = row.find("TD").eq(4).html();
            purchase_contrl_type_dic.purchase_control_guid = row.find("TD").eq(5).html();
            var data = '';
            if (purchase_contrl_type_dic.purchase_ctrl_flag == 'Activate'){
                data = true
            } else{
                data = false
            }
            purchase_contrl_type_dic.purchase_ctrl_flag  = data;
            main_table_purchase_contrl_checked.push(purchase_contrl_type_dic);
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
        main_attribute.company_code_id = row.find("TD").eq(1).html();
        main_attribute.call_off = row.find("TD").eq(2).html();
        main_attribute.prod_cat_id = row.find("TD").eq(3).html();
        if (!main_table_data.hasOwnProperty(main_attribute.company_code_id)) {
            main_table_data[main_attribute.company_code_id] = [];
        }
        main_table_data[main_attribute.company_code_id].push({
            call_off: main_attribute.call_off,
            prod_cat_id: main_attribute.prod_cat_id,
        });
    });
    table_sort_filter('display_basic_table');
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html +=
    `<tr>
        <td><input type="checkbox" required></td>
        <td><select class="input form-control" type="text" onchange="get_call_off(this)">${pc_company_dropdown}</select></td>
        <td><select class="input form-control" type="text" onchange="get_prod_cat_id_values(this)">${call_off_dropdown}</select></td>
        <td><select class="form-control">${prod_cat_dropdown}</select></td>
        <td><select type="text" class="input form-control">${activate_dropdown}</select></td>
        <td hidden><input  type="text" class="form-control"  name="guid"></td>
        <td class="class_del_checkbox" hidden><input type="checkbox" required></td>
    </tr>`
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

// onchange respective values for company dropdown
function get_call_off(selectElement) {
    var selected_call_off = selectElement.value;
    var call_off_dropdown = $(selectElement).closest('tr').find('.form-control').eq(1);
    var prod_cat_dropdown = $(selectElement).closest('tr').find('.form-control').eq(2);

    call_off_dropdown.empty(); // Clear existing options
    prod_cat_dropdown.empty(); // Clear existing options

    var call_off_values = main_table_data[selected_call_off];
    if (!call_off_values) {
        call_off_dropdown.empty();
        $.each(rendered_call_off, function (i, item) {
            call_off_dropdown.append('<option value="' + item.value + '">' + item.desc + '</option>')
        });

        prod_cat_dropdown.empty();
        $.each(rendered_prod_category, function (i, item) {
            prod_cat_dropdown.append('<option value="' + item.prod_cat_id + '">' + item.prod_cat_id + '</option>')
        });
        return;
    }

    // Stored respective dropdown values for particular company id
    main_table_call_off = {};
    call_off_values.forEach(item => {
        var call_off = item.call_off ;
        if (!main_table_call_off[call_off ]) {
            main_table_call_off[call_off ] = new Set();
        }
        main_table_call_off[call_off ].add(item.prod_cat_id);
    });

    // Filtering CALL_OFF dropdown
    hiddenCallOffValue = [];
    for (const item of rendered_call_off) {
        const callOffValue = item.desc;

        if (rendered_prod_category.length === main_table_call_off[callOffValue]?.size) {
            hiddenCallOffValue.push(callOffValue);
        } else {
            call_off_dropdown.append('<option value="' + callOffValue + '">' + callOffValue + '</option>');
        }
    }

    // Filtering UNSPSC values
    hidden_prod_cat_IDs = [];
    var callOffValuesArray = call_off_dropdown.html().match(/value="([^"]+)"/g).map(function(match) {
        return match.match(/"([^"]+)"/)[1];
    });
    for (var i = 0; i < callOffValuesArray.length; i++) {
        var callOffValue = callOffValuesArray[i];
        if (!main_table_call_off.hasOwnProperty(callOffValue)){
            prod_cat_dropdown.empty();
            $.each(rendered_prod_category, function (i, item) {
                prod_cat_dropdown.append('<option value="' + item.prod_cat_id + '">' + item.prod_cat_id + '</option>')
            });
            break;
        } else if (main_table_call_off.hasOwnProperty(callOffValue)) {
            var assignedProdCatIDs = Array.from(main_table_call_off[callOffValue]);
            rendered_prod_category.forEach(function(item) {
                var prod_cat_id = item.prod_cat_id;
                if (!assignedProdCatIDs.includes(prod_cat_id)) {
                    prod_cat_dropdown.append('<option value="' + prod_cat_id + '">' + prod_cat_id + '</option>') ;
                }
            });
            break;
        }
    }
}

// onchange respective values for call_off dropdown
function get_prod_cat_id_values(selectElement) {
    var selected_call_off = selectElement.value;
    var company_id = $(selectElement).closest('tr').find('.form-control').eq(0).val();
    var prod_cat_dropdown = $(selectElement).closest('tr').find('.form-control').eq(2);
    prod_cat_dropdown.empty(); // Clear existing options

    var call_off_values = main_table_data[company_id];
    main_table_call_off = {};
    if (!call_off_values) {
        prod_cat_dropdown.empty();
        $.each(rendered_prod_category, function (i, item) {
            prod_cat_dropdown.append('<option value="' + item.prod_cat_id + '">' + item.prod_cat_id + '</option>')
        });
        return;
    }

    call_off_values.forEach(item => {
        var call_off = item.call_off ;
        if (!main_table_call_off[call_off ]) {
            main_table_call_off[call_off ] = new Set();
        }
        main_table_call_off[call_off ].add(item.prod_cat_id);
    });

    if (!main_table_call_off.hasOwnProperty(selected_call_off)){
        $.each(rendered_prod_category, function (i, item) {
            prod_cat_dropdown.append('<option value="' + item.prod_cat_id + '">' + item.prod_cat_id + '</option>')
        });
        return;
    } else if (main_table_call_off.hasOwnProperty(selected_call_off)) {
        var assignedProdCatIDs = Array.from(main_table_call_off[selected_call_off]);
        rendered_prod_category.forEach(function(item) {
            var prod_cat_id = item.prod_cat_id;
            if (!assignedProdCatIDs.includes(prod_cat_id)) {
                prod_cat_dropdown.append('<option value="' + prod_cat_id + '">' + prod_cat_id + '</option>')
            }
        });
        return;
    }
}
