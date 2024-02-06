var po_split_criteria_data = new Array();
var validate_add_attributes = [];
var po_split_criteria={};
var split_type_array = new Array();
var main_table_low_value = [];

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#po_criteria_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_client").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_client_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#po_criteria_Modal').modal('hide');
    po_split_criteria_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    po_split_criteria_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        po_split_criteria={};
        po_split_criteria.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        po_split_criteria.activate = row.find("TD").eq(3).find('select[type="text"]').val();
        po_split_criteria.company_code_id = row.find("TD").eq(2).find('select[type="text"]').val();
        po_split_criteria.po_split_type = parseInt(row.find("TD").eq(1).find('select[type="text"]').val());
        po_split_criteria.po_split_criteria_guid = row.find("TD").eq(4).find('input[type="text"]').val();
        if (po_split_criteria == undefined){
            po_split_criteria.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        var data = '';
        if (po_split_criteria.activate == 'Activate'){
            data = true
        } else{
            data = false
        }
        po_split_criteria.activate  = data;
        var compare = po_split_criteria.po_split_type + '-' + po_split_criteria.company_code_id
        validate_add_attributes.push(compare);
        po_split_criteria_data.push(po_split_criteria);
    });
    table_sort_filter('id_popup_table');
    return po_split_criteria_data;
}

//************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#po_criteria_Modal').modal('show');
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html =
        '<tr><td><input type="checkbox" required></td>'+
        '<td><select type="text" class="input form-control" onchange="get_company_values(this)">'+ po_split_type_dropdown +'</select></td>'+
        '<td><select type="text" class="input form-control">'+ company_dropdown +'</select></td><td><select type="text" class="input form-control">'+ activate_dropdown +'</select></td><td hidden><input type="text" class= "form-control" name="po_split_criteria_guid"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}

function get_company_values(selectElement) {
    var selected_company = selectElement.value;
    var companyDropdown = $(selectElement).closest('tr').find('.form-control').eq(1);
    var company = main_table_data[selected_company];
    var used_companyValues = {}; // Object to store the used node values for the selected node type

    // Loop through the node values in the main_table_data and store the used ones for the selected node type
    $.each(company, function (index, value) {
        used_companyValues[value] = true;
    });

    companyDropdown.empty();

    // Now, populate the dropdown with only the unused node values from rendered_call_off_data.data
    $.each(rendered_company_data, function (i, item) {
        var companyValue = item.company_id;
        if (!used_companyValues.hasOwnProperty(companyValue)) {
            companyDropdown.append('<option value="' + companyValue + '">' + companyValue + '</option>');
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
        main_attribute.po_split_type = parseInt(row.find("TD").eq(1).html());
        main_attribute.company_code_id = row.find("TD").eq(2).html();
        main_attribute.activate = row.find("TD").eq(3).html();
        var data = '';
        if (main_attribute.activate == 'Activate'){
            data = true
        } else{
            data = false
        }
        main_attribute.activate  = data;
        main_attribute.po_split_criteria_guid = row.find("TD").eq(4).html();
        var compare_maintable = main_attribute.po_split_type + '-' + main_attribute.company_code_id
        main_table_low_value.push(compare_maintable);
    });
    table_sort_filter_page('display_basic_table');
}

// Function to get the selected row data
function get_selected_row_data(){
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var aac_arr_obj = {};
        split_type_array = [];
        aac_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
        if(aac_arr_obj.del_ind) {
            aac_arr_obj.po_split_type = row.find("TD").eq(1).html();
            aac_arr_obj.company_code_id = row.find("TD").eq(2).html();
            aac_arr_obj.activate = row.find("TD").eq(3).html();
            aac_arr_obj.po_split_criteria_guid = row.find("TD").eq(4).html();
            var data = '';
            if (aac_arr_obj.activate == 'Activate') {
                data = true
            } else{
                data = false
            }
            aac_arr_obj.activate  = data;
            split_type_array = (aac_arr_obj.po_split_type).split(" -");
            aac_arr_obj.po_split_type = split_type_array[0];
            main_table_po_crt_checked.push(aac_arr_obj);
        }
    });
}

function get_split_type_data() {
    main_table_data = {}; // Object to store node values for each node type
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.po_split_type = parseInt(row.find("TD").eq(1).html());
        main_attribute.company_code_id = row.find("TD").eq(2).html();
        var compare_maintable = main_attribute.po_split_type + '-' + main_attribute.company_code_id
        if (!main_table_data.hasOwnProperty(main_attribute.po_split_type)) {
            main_table_data[main_attribute.po_split_type] = [];
        }
        main_table_data[main_attribute.po_split_type].push(main_attribute.company_code_id);
    });
    table_sort_filter('display_basic_table');
}