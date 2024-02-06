var po_split_type_data = new Array();
var validate_add_attributes = [];
var po_split_types={};
var main_table_low_value = [];

//hide the myModal popup: Implemented Dependency delete purpose
function hideModal() {
    $('#potype_Modal').modal('hide');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#potype_Modal').modal('hide');
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

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_po_sp_ty_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_aac_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.po_split_type + '</td><td>' + item.po_split_type_desc + '</td></tr>';
    });
    $('#id_po_sp_ty_tbody').append(edit_basic_data);
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

//Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#potype_Modal').modal('hide');
    po_split_type_data = read_popup_data();
    $('#id_save_confirm_popup').modal('show');
});

//Read popup table data
function read_popup_data() {
    $('#id_popup_table').DataTable().destroy();
    po_split_type_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        po_split_types={};
        po_split_types.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        po_split_types.po_split_type_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        po_split_types.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
        if (po_split_types == undefined){
            po_split_types.po_split_type = row.find("TD").eq(1).find('select[type="text"]').val();
            }
        validate_add_attributes.push(po_split_types.po_split_type);
        po_split_type_data.push(po_split_types);
    });
    table_sort_filter('id_popup_table');
    return po_split_type_data;
}

// function to display erroe msg
function display_error_message(error_message){
    $('#error_message').text(error_message);
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#potype_Modal').modal('show');
}

// Function to get main table data
function get_main_table_data(){
    main_table_low_value = [];
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function() {
        var row = $(this);
        var main_attribute = {};
        main_attribute.po_split_type = row.find("TD").eq(1).html();
        main_table_low_value.push(main_attribute.po_split_type);
    });
    table_sort_filter_page('display_basic_table');
}

// Function to get the selected row data
function get_row_data(tableSelector) {
    main_table_po_split_checked = []; // Clear the previous data before collecting new data
    $(tableSelector).DataTable().$('input[type="checkbox"]').each(function () {
        var checkbox = $(this);
        var row = checkbox.closest("tr");
        var po_split_type_dic = {};
        po_split_type_dic.del_ind = checkbox.is(':checked');
        if(po_split_type_dic.del_ind) {
            po_split_type_dic.po_split_type = row.find("TD").eq(1).find('input[type="text"]').val() || row.find("TD").eq(1).html();
            po_split_type_dic.po_split_type_desc = row.find("TD").eq(2).find('input[type="text"]').val() || row.find("TD").eq(2).html();
            main_table_po_split_checked.push(po_split_type_dic);
        }
    });
}

// Function for add a new row data
function new_row_data(){
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
        '<td><select type="text" class="input form-control aaccode"  name="aaccode" onchange="GetSelectedTextValue(this)">' +aac_dropdown +'</select></td>'+
        '<td><input class="form-control description" type="text"  name="description" value="'+desc_aac+'"  disabled></td>'+
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
        table_sort_filter('id_popup_table');
        var aaccodeSelect = $("#aaccode-1");
    }