var doctype_data = new Array();
var validate_add_attributes = [];
var main_table_low_value = [];
var doctype ={};

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#doc_Modal').modal('hide');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#doc_Modal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_doctype_code").prop("hidden", true);
    $("#id_error_msg_doctype_name").prop("hidden", true);
    $("#id_error_msg_doctype_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//********************************************
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#doc_Modal').modal('show');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_doctype_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_doctype_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.document_type + '</td><td>' + item.document_type_desc + '</td></tr>';
    });
    $('#id_doctype_tbody').append(edit_basic_data);
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

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#doc_Modal').modal('hide');
    doctype_data  = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    doctype_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        doctype = {};
        doctype.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        doctype.document_type_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        doctype.document_type = row.find("TD").eq(1).find('select[type="text"]').val();
        if (doctype == undefined) {
            doctype.document_type = row.find("TD").eq(1).find('select[type="text"]').val();
        }
        validate_add_attributes.push(doctype.document_type);
        doctype_data.push(doctype);
    });
    table_sort_filter('id_popup_table');
    return doctype_data;
}

// Function to get the selected row data
function get_row_data(tableSelector){
    main_table_doctype_checked = [];
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var doctype_arr_obj = {};
        doctype_arr_obj.del_ind = checkbox.is(':checked');
        if(doctype_arr_obj.del_ind){
            doctype_arr_obj.document_type = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            doctype_arr_obj.document_type_desc = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            main_table_doctype_checked.push(doctype_arr_obj);
        }
    });
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var main_attribute = {};
        main_attribute.document_type = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.document_type);
    });
    table_sort_filter('display_basic_table');
}

// Function for add a new row data
function new_row_data() {
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="input form-control documenttype" name="documenttype" onchange="GetSelectedTextValue(this)">'+ document_type_dropdown +'</select></td>'+
    '<td><input class="form-control description" type="text" value="'+doc_desc+'" name="description" disabled></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
}